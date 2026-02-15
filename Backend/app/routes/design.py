from fastapi import APIRouter, Depends, HTTPException, status, BackgroundTasks
from sqlalchemy.orm import Session
from typing import List
import uuid

from app.database import get_db
from app.dependencies import get_current_user
from app.schemas.design import (
    DesignGenerateRequest, 
    DesignGenerateResponse, 
    DesignResponse,
    DesignListResponse,
    DesignWithDetails
)
from app.models.design import Design as DesignModel
from app.models.room import Room as RoomModel
from app.models.user import User as UserModel
from app.services.ai_engine import get_ai_engine
from app.services.vastu_engine import get_vastu_engine
from app.services.budget_engine import get_budget_engine

router = APIRouter(prefix="/api/design", tags=["design"])


def generate_design_task(
    design_id: str,
    room_id: str,
    user_id: str,
    style: str,
    budget: float,
    room_type: str,
    direction: str
):
    """Background task to generate design"""
    from app.database import SessionLocal
    db = SessionLocal()
    
    try:
        # Get room image
        room = db.query(RoomModel).filter(RoomModel.id == room_id).first()
        if not room:
            return
        
        # Generate AI designs
        design_urls = get_ai_engine().generate_design_variations(
            room.image_url, 
            style, 
            room_type or "living"
        )
        
        # Calculate budget
        budget_data = get_budget_engine().calculate_estimate(
            room_type or "living", 
            style, 
            budget
        )
        
        # Vastu analysis
        vastu_data = get_vastu_engine().analyze(direction or "north", room_type or "living")
        
        # Update design record
        design = db.query(DesignModel).filter(DesignModel.id == design_id).first()
        if design:
            design.image_1_url = design_urls[0] if len(design_urls) > 0 else None
            design.image_2_url = design_urls[1] if len(design_urls) > 1 else None
            design.image_3_url = design_urls[2] if len(design_urls) > 2 else None
            design.estimated_cost = budget_data["estimated_cost"]
            design.budget_match_percentage = budget_data["budget_match_percentage"]
            design.furniture_breakdown = budget_data["furniture_breakdown"]
            design.vastu_score = vastu_data["vastu_score"]
            design.vastu_suggestions = vastu_data["suggestions"]
            design.vastu_warnings = vastu_data["warnings"]
            design.status = "completed"
            
            db.commit()
    except Exception as e:
        # Update status to failed
        design = db.query(DesignModel).filter(DesignModel.id == design_id).first()
        if design:
            design.status = "failed"
            db.commit()
    finally:
        db.close()


@router.post("/generate", response_model=DesignGenerateResponse)
async def generate_design(
    request: DesignGenerateRequest,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """
    Generate design variations for a room
    """
    # Check if room exists and belongs to user
    room = db.query(RoomModel).filter(
        RoomModel.id == request.room_id,
        RoomModel.user_id == current_user["uid"]
    ).first()
    
    if not room:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Room not found"
        )
    
    # Create design record
    design_id = str(uuid.uuid4())
    design = DesignModel(
        id=design_id,
        room_id=request.room_id,
        user_id=current_user["uid"],
        style=request.style,
        budget=request.budget,
        status="pending"
    )
    
    db.add(design)
    db.commit()
    db.refresh(design)
    
    # Start background task
    background_tasks.add_task(
        generate_design_task,
        design_id,
        request.room_id,
        current_user["uid"],
        request.style,
        request.budget,
        room.room_type,
        room.direction
    )
    
    return DesignGenerateResponse(
        design_id=design_id,
        status="pending",
        message="Design generation started. Check status in a few moments."
    )


@router.get("/{design_id}", response_model=DesignResponse)
async def get_design(
    design_id: str,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """
    Get design details by ID
    """
    design = db.query(DesignModel).filter(
        DesignModel.id == design_id,
        DesignModel.user_id == current_user["uid"]
    ).first()
    
    if not design:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Design not found"
        )
    
    return design


@router.get("/room/{room_id}", response_model=DesignListResponse)
async def get_room_designs(
    room_id: str,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """
    Get all designs for a room
    """
    # Verify room belongs to user
    room = db.query(RoomModel).filter(
        RoomModel.id == room_id,
        RoomModel.user_id == current_user["uid"]
    ).first()
    
    if not room:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Room not found"
        )
    
    designs = db.query(DesignModel).filter(
        DesignModel.room_id == room_id
    ).order_by(DesignModel.created_at.desc()).all()
    
    return DesignListResponse(designs=designs, total=len(designs))


@router.get("/room/{room_id}/with-details")
async def get_room_designs_with_details(
    room_id: str,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """
    Get all designs for a room with full details including budget and vastu
    """
    # Verify room belongs to user
    room = db.query(RoomModel).filter(
        RoomModel.id == room_id,
        RoomModel.user_id == current_user["uid"]
    ).first()
    
    if not room:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Room not found"
        )
    
    designs = db.query(DesignModel).filter(
        DesignModel.room_id == room_id
    ).order_by(DesignModel.created_at.desc()).all()
    
    result = []
    for design in designs:
        budget_summary = {
            "estimated_cost": design.estimated_cost,
            "budget": design.budget,
            "budget_match_percentage": design.budget_match_percentage,
            "furniture_breakdown": design.furniture_breakdown
        } if design.furniture_breakdown else None
        
        result.append({
            "design": design,
            "room_image_url": room.image_url,
            "budget_summary": budget_summary
        })
    
    return {"designs": result, "total": len(result), "room": room}
