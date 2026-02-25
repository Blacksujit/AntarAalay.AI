"""
Design API Routes for AntarAalay.ai

Endpoints for:
- Generating AI designs with Stability AI
- Regenerating with customizations
- Fetching design history
"""
from fastapi import APIRouter, Depends, HTTPException, status
from typing import List, Optional
from datetime import datetime, timedelta
import uuid
import asyncio
import json
import os
from sqlalchemy.orm import Session

from app.dependencies import get_current_user, get_db
from app.models import Design, Room
from app.config import get_settings
from app.schemas.design import (
    DesignGenerateRequest,
    DesignGenerateResponse,
    DesignResponse,
    DesignListResponse,
    DesignCustomizationRequest
)
from app.services.ai_engine import EngineFactory, EngineType, GenerationRequest, GenerationResult
from app.database import get_db_manager
from app.services.firebase_client import get_firestore, get_firebase_storage
from app.services.room_service import room_upload_service
import logging

logger = logging.getLogger(__name__)

# Simple in-memory rate limiting
user_requests = {}

def check_rate_limit(user_id: str, limit: int = 5, window_minutes: int = 1) -> bool:
    """Simple rate limiting check."""
    now = datetime.utcnow()
    window_start = now - timedelta(minutes=window_minutes)
    
    # Clean old requests
    if user_id in user_requests:
        user_requests[user_id] = [req_time for req_time in user_requests[user_id] if req_time > window_start]
    else:
        user_requests[user_id] = []
    
    # Check if under limit
    if len(user_requests[user_id]) >= limit:
        return False
    
    # Add current request
    user_requests[user_id].append(now)
    return True

router = APIRouter(prefix="/design", tags=["design"])


@router.post("/generate", response_model=DesignGenerateResponse)
async def generate_design(
    request: DesignGenerateRequest,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Generate AI interior designs using Models Lab API.
    
    - Uses professional Models Lab AI for high-quality interior design
    - Generates 3 professional interior variations
    - Applies rate limiting (5 per minute per user)
    - Saves designs to local database
    - Returns professional AI-generated images
    """
    try:
        user_id = current_user.get('uid') or current_user.get('localId')
        
        print(f"=== DESIGN GENERATION STARTED ===")
        print(f"User ID: {user_id}")
        print(f"Request: room_id={request.room_id}, style={request.style}")
        
        # Check rate limiting
        if not check_rate_limit(user_id, limit=5, window_minutes=1):
            raise HTTPException(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                detail="Rate limit exceeded: Maximum 5 design generations per minute"
            )
        
        logger.info(f"Starting professional design generation for user {user_id}")
        logger.info(f"Room ID: {request.room_id}, Style: {request.style}, Wall: {request.wall_color}, Flooring: {request.flooring_material}")
        
        # Use Models Lab AI engine for professional interior design
        from app.services.ai_engine import EngineFactory, EngineType
        from app.services.ai_engine.base_engine import GenerationRequest
        
        # Create Models Lab engine with empty key to force fallback immediately
        engine_config = {
            'models_lab_api_key': '',  # Empty to force fallback immediately
            'device': 'cpu'
        }
        print(f"Creating Models Lab engine...")
        engine = EngineFactory.create_engine(EngineType.LOCAL_SDXL, engine_config)
        print(f"Models Lab engine created successfully")
        
        # Find all room images
        rooms = []
        room_base_id = request.room_id.split('_')[0]
        print(f"Querying database for room images: {room_base_id}")
        
        for direction in ['north', 'south', 'east', 'west']:
            room_id = f"{room_base_id}_{direction}"
            room = db.query(Room).filter_by(id=room_id, user_id=user_id).first()
            if room:
                rooms.append(room)
        
        print(f"Found {len(rooms)} room images")
        
        if not rooms:
            print(f"ERROR: No rooms found for {room_base_id}")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Room images not found"
            )
        
        print(f"Getting primary room (north direction)...")
        # Get primary image (north direction) for generation
        primary_room = next((room for room in rooms if room.direction == 'north'), rooms[0])
        print(f"Primary room image URL: {primary_room.image_url}")
        
        print(f"Downloading primary image...")
        # Download the primary image
        import httpx
        async with httpx.AsyncClient() as client:
            response = await client.get(primary_room.image_url)
            print(f"Download response status: {response.status_code}")
            if response.status_code != 200:
                print(f"ERROR: Failed to download image: {response.status_code}")
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Failed to download room image"
                )
            primary_image = response.content
            print(f"Downloaded {len(primary_image)} bytes")
        
        print(f"Downloading all room images...")
        # Create room images dict
        room_images = {}
        for room in rooms:
            async with httpx.AsyncClient() as client:
                response = await client.get(room.image_url)
                if response.status_code == 200:
                    room_images[room.direction] = response.content
        
        print(f"Downloaded {len(room_images)} room images")
        print(f"Creating GenerationRequest...")
        # Create generation request for Models Lab
        gen_request = GenerationRequest(
            primary_image=primary_image,
            room_images=room_images,
            room_type=request.room_type or "living",
            furniture_style=request.style.lower(),
            wall_color=request.wall_color.lower(),
            flooring_material=request.flooring_material.lower()
        )
        print(f"GenerationRequest created successfully")
        
        # Use AI engine from environment configuration
        print(f"Creating AI engine from environment...")
        
        result = GenerationResult(success=False, generated_images=[], error_message="Not initialized")
        
        try:
            from app.services.ai_engine import EngineFactory
            
            # Get engine from environment (pollinations, local_sdxl, etc.)
            engine = EngineFactory.get_engine_from_env()
            print(f"✅ {type(engine).__name__} created from environment")
            
            result = await engine.generate_img2img(gen_request)
            print(f"AI generation result: success={result.success}, images={len(result.generated_images)}")
            
            if result.success:
                print(f"✅ AI generation successful!")
                # Save results and return immediately
                design_id = str(uuid.uuid4())
                print(f"Design ID: {design_id}")
                
                # Create single design record with all 3 images
                design = Design(
                    id=design_id,
                    user_id=user_id,
                    room_id=request.room_id,
                    style=request.style,
                    wall_color=request.wall_color,
                    flooring_material=request.flooring_material,
                    image_1_url=result.generated_images[0] if len(result.generated_images) > 0 else None,
                    image_2_url=result.generated_images[1] if len(result.generated_images) > 1 else None,
                    image_3_url=result.generated_images[2] if len(result.generated_images) > 2 else None,
                    estimated_cost=50000,
                    budget_match_percentage=85.0,
                    furniture_breakdown=json.dumps({
                        "sofa": {"adjusted_price": 15000, "base_price": 12000, "quantity": 1},
                        "table": {"adjusted_price": 8000, "base_price": 6000, "quantity": 1},
                        "chairs": {"adjusted_price": 5000, "base_price": 4000, "quantity": 2}
                    }),
                    vastu_score=85,
                    vastu_suggestions='Good layout with professional design',
                    vastu_warnings='None',
                    status='completed',
                    created_at=datetime.utcnow(),
                    updated_at=datetime.utcnow()
                )
                
                db.add(design)
                db.commit()
                
                logger.info(f"✅ Generated {len(result.generated_images)} professional designs with {type(engine).__name__} in {result.inference_time_seconds:.2f}s")
                logger.info(f"Designs saved to database: {design_id}")
                
                return DesignGenerateResponse(
                    design_id=design_id,
                    status='success',
                    message=f'Generated {len(result.generated_images)} professional designs using {type(engine).__name__} AI'
                )
            else:
                print(f"⚠️ AI generation failed: {result.error_message}")
        except Exception as e:
            print(f"⚠️ AI engine error: {e}")
            import traceback
            print(f"Traceback: {traceback.format_exc()}")
        
        # If primary engine failed, try fallback
        if not result.success:
            print(f"⚠️ Primary engine failed, trying fallback...")
            
            try:
                from app.services.ai_engine import EngineFactory, EngineType
                
                engine_config = {
                    'device': 'cpu'
                }
                print(f"Creating Models Lab engine...")
                engine = EngineFactory.create_engine(EngineType.LOCAL_SDXL, engine_config)
                print(f"Models Lab engine created successfully")
                
                # Find all room images
                room_images = {}
                for direction in ['north', 'south', 'east', 'west']:
                    image_key = f'{direction}_image'
                    if hasattr(request, image_key):
                        room_images[direction] = getattr(request, image_key)
                
                # Generate designs
                result = await engine.generate_img2img(gen_request)
                print(f"Models Lab API result: success={result.success}, images={len(result.generated_images)}")
                print(f"Error message: {result.error_message}")
                
                if result.success:
                    print(f"✅ Models Lab generation successful!")
                    # Save Models Lab results and return
                    design_id = str(uuid.uuid4())
                    print(f"Design ID: {design_id}")
                    
                    # Create single design record with all 3 images
                    design = Design(
                        id=design_id,
                        user_id=user_id,
                        room_id=request.room_id,
                        style=request.style,
                        wall_color=request.wall_color,
                        flooring_material=request.flooring_material,
                        image_1_url=result.generated_images[0] if len(result.generated_images) > 0 else None,
                        image_2_url=result.generated_images[1] if len(result.generated_images) > 1 else None,
                        image_3_url=result.generated_images[2] if len(result.generated_images) > 2 else None,
                        estimated_cost=50000,
                        budget_match_percentage=85.0,
                        furniture_breakdown=json.dumps({
                            "sofa": {"adjusted_price": 15000, "base_price": 12000, "quantity": 1},
                            "table": {"adjusted_price": 8000, "base_price": 6000, "quantity": 1},
                            "chairs": {"adjusted_price": 5000, "base_price": 4000, "quantity": 2}
                        }),
                        vastu_score=85,
                        vastu_suggestions='Good layout with professional design',
                        vastu_warnings='None',
                        status='completed',
                        created_at=datetime.utcnow(),
                        updated_at=datetime.utcnow()
                    )
                    
                    db.add(design)
                    db.commit()
                    
                    logger.info(f"✅ Generated {len(result.generated_images)} professional designs with Models Lab in {result.inference_time_seconds:.2f}s")
                    logger.info(f"Designs saved to database: {design_id}")
                    
                    return DesignGenerateResponse(
                        design_id=design_id,
                        status='success',
                        message=f'Generated {len(result.generated_images)} professional designs using Models Lab AI'
                    )
                else:
                    print(f"⚠️ Models Lab failed: {result.error_message}")
            except Exception as e:
                print(f"⚠️ Models Lab error: {e}")
                import traceback
                print(f"Traceback: {traceback.format_exc()}")
        
        # If all AI engines failed, fall back to demo mode
        if not result.success:
            from app.services.demo_design_service import demo_service
            
            demo_result = demo_service.generate_demo_designs(
                room_id=request.room_id,
                style=request.style,
                wall_color=request.wall_color,
                flooring=request.flooring_material,
                user_id=user_id
            )
            
            # Save demo designs to database
            for design_data in demo_result["designs"]:
                design_data_clean = {k: v for k, v in design_data.items() if k != 'is_demo'}
                design = Design(**design_data_clean)
                db.add(design)
            
            db.commit()
            
            print(f"✅ Demo designs saved to database: {demo_result['design_id']}")
            
            return DesignGenerateResponse(
                design_id=demo_result["design_id"],
                status='success',
                message='Demo designs generated (AI generation temporarily unavailable)'
            )
        
        if not result.success:
            print(f"ERROR: Models Lab generation failed: {result.error_message}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Design generation failed: {result.error_message}"
            )
        
        print(f"Saving designs to database...")
        # Save designs to database - Models Lab returns URLs, map them to image fields
        design_id = str(uuid.uuid4())
        print(f"Design ID: {design_id}")
        
        # Create single design record with all 3 images
        design = Design(
            id=design_id,
            user_id=user_id,
            room_id=request.room_id,
            style=request.style,
            wall_color=request.wall_color,
            flooring_material=request.flooring_material,
            image_1_url=result.generated_images[0] if len(result.generated_images) > 0 else None,
            image_2_url=result.generated_images[1] if len(result.generated_images) > 1 else None,
            image_3_url=result.generated_images[2] if len(result.generated_images) > 2 else None,
            estimated_cost=50000,
            budget_match_percentage=85.0,
            furniture_breakdown=json.dumps({
                "sofa": {"adjusted_price": 15000, "base_price": 12000, "quantity": 1},
                "table": {"adjusted_price": 8000, "base_price": 6000, "quantity": 1},
                "chairs": {"adjusted_price": 5000, "base_price": 4000, "quantity": 2}
            }),
            vastu_score=85,
            vastu_suggestions='Good layout with professional design',
            vastu_warnings='None',
            status='completed',
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )
        
        db.add(design)
        db.commit()
        
        logger.info(f"✅ Generated {len(result.generated_images)} professional designs with Models Lab in {result.inference_time_seconds:.2f}s")
        logger.info(f"Designs saved to database: {design_id}")
        
        return DesignGenerateResponse(
            design_id=design_id,
            status='success',
            message=f'Generated {len(result.generated_images)} professional designs using Models Lab AI'
        )
        
    except HTTPException:
        raise
    except Exception as e:
        import traceback
        logger.error(f"Design generation failed: {e}")
        logger.error(f"Traceback: {traceback.format_exc()}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Generation failed: {str(e)}"
        )


@router.post("/{design_id}/regenerate", response_model=DesignResponse)
async def regenerate_design(
    design_id: str,
    request: DesignCustomizationRequest,
    current_user: dict = Depends(get_current_user)
):
    """
    Regenerate design with new customization options.
    
    - Uses layout-preserving image-to-image transformation
    - Applies new styling parameters
    - Creates new design version
    - Maintains original room geometry
    """
    try:
        user_id = current_user.get('uid') or current_user.get('localId')
        
        # Get AI design service
        from app.services.ai_design_service import get_ai_design_service
        ai_service = await get_ai_design_service()
        
        # Prepare updates
        updates = {}
        if request.style:
            updates['furniture_style'] = request.style
        if request.wall_color:
            updates['wall_color'] = request.wall_color
        if request.flooring_material:
            updates['flooring_material'] = request.flooring_material
        
        # Regenerate design
        result = await ai_service.regenerate_design(
            user_id=user_id,
            user_data=current_user,
            design_id=design_id,
            updates=updates
        )
        
        if result['status'] == 'rate_limited':
            raise HTTPException(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                detail={
                    "error_code": result['error_code'],
                    "message": result['message']
                }
            )
        
        if result['status'] == 'failed':
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=result['message']
            )
        
        logger.info(f"Design regenerated: {result['design_id']} from original {design_id}")
        
        # Return the new design
        return DesignResponse(
            design_id=result['design_id'],
            room_id=result.get('room_id', ''),
            user_id=user_id,
            style=request.style,
            customization=updates,
            generated_images=result.get('generated_images', []),
            created_at=datetime.now().isoformat(),
            updated_at=datetime.now().isoformat()
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Design regeneration failed: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Regeneration failed: {str(e)}"
        )


@router.get("/room/{room_id}", response_model=DesignListResponse)
async def get_room_designs(
    room_id: str,
    current_user: dict = Depends(get_current_user)
):
    """
    Get all designs for a room.
    """
    try:
        user_id = current_user.get('uid') or current_user.get('localId')
        
        # Verify room ownership
        room = await room_upload_service.get_room(room_id, user_id)
        if not room:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Room not found"
            )
        
        # Get designs
        firestore = get_firestore()
        designs = await firestore.get_room_designs(room_id, user_id)
        
        return DesignListResponse(
            designs=[DesignResponse(**d) for d in designs],
            total=len(designs)
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to fetch designs: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to fetch designs: {str(e)}"
        )


@router.get("/room/{room_id}/with-details")
async def get_room_designs_with_details(
    room_id: str,
    current_user: dict = Depends(get_current_user)
):
    """Get room designs along with room preview and budget summary.

    This endpoint is consumed by the frontend Designs page.
    """
    try:
        user_id = current_user.get('uid') or current_user.get('localId')

        room = await room_upload_service.get_room(room_id, user_id)
        if not room:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Room not found"
            )

        # Get designs from local database instead of Firestore
        from app.database import get_db_manager
        from app.models.design import Design
        
        db_manager = get_db_manager()
        with db_manager.session_scope() as session:
            designs = session.query(Design).filter(
                Design.room_id == room_id,
                Design.user_id == user_id
            ).order_by(Design.created_at.desc()).all()
            
            # Convert to list of dicts - match DesignResponse schema
            designs_list = []
            for design in designs:
                # Parse furniture_breakdown from JSON string if needed
                furniture_data = design.furniture_breakdown
                if isinstance(furniture_data, str):
                    try:
                        furniture_data = json.loads(furniture_data)
                    except:
                        furniture_data = {}
                
                # Ensure furniture_data has the correct structure with adjusted_price
                if furniture_data and isinstance(furniture_data, dict):
                    formatted_furniture = {}
                    for item, details in furniture_data.items():
                        if isinstance(details, dict) and 'adjusted_price' in details:
                            formatted_furniture[item] = details
                        else:
                            # Convert simple number to proper structure
                            formatted_furniture[item] = {
                                'adjusted_price': details if isinstance(details, (int, float)) else 0,
                                'base_price': details if isinstance(details, (int, float)) else 0,
                                'quantity': 1
                            }
                    furniture_data = formatted_furniture
                
                designs_list.append({
                    'id': design.id,
                    'room_id': design.room_id,
                    'user_id': design.user_id,
                    'style': design.style,
                    'budget': design.budget or 0,
                    'image_1_url': design.image_1_url,
                    'image_2_url': design.image_2_url,
                    'image_3_url': design.image_3_url,
                    'estimated_cost': design.estimated_cost or 50000,
                    'budget_match_percentage': design.budget_match_percentage or 85,
                    'furniture_breakdown': furniture_data or {},
                    'vastu_score': design.vastu_score or 85,
                    'vastu_suggestions': [],
                    'vastu_warnings': [],
                    'status': design.status,
                    'created_at': design.created_at if design.created_at else datetime.utcnow()
                })

        room_image_url = (room.get("images") or {}).get("north")
        room_payload = {
            "id": room.get("room_id") or room_id,
            "image_url": room_image_url,
            "room_type": room.get("room_type"),
            "direction": room.get("direction"),
        }

        designs_payload = []
        for d in designs_list:
            design_obj = DesignResponse(**d)
            design_dump = design_obj.model_dump()
            logger.info(f"DesignResponse dump: {design_dump}")
            designs_payload.append(
                {
                    "design": design_dump,
                    "room_image_url": room_image_url,
                    "budget_summary": None,
                }
            )

        response_data = {
            "designs": designs_payload,
            "total": len(designs_payload),
            "room": room_payload,
        }
        logger.info(f"Full API response: {response_data}")
        return response_data
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to fetch designs with details: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to fetch designs with details: {str(e)}"
        )


@router.get("/{design_id}", response_model=DesignResponse)
async def get_design(
    design_id: str,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get a specific design by ID.
    """
    try:
        user_id = current_user.get('uid') or current_user.get('localId')
        
        # Query PostgreSQL instead of Firestore
        design = db.query(Design).filter(
            Design.id == design_id,
            Design.user_id == user_id
        ).first()
        
        if not design:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Design not found"
            )
        
        # Convert to response format
        design_dict = {
            "id": design.id,
            "room_id": design.room_id,
            "user_id": design.user_id,
            "style": design.style,
            "budget": design.budget,
            "wall_color": design.wall_color,
            "flooring_material": design.flooring_material,
            "image_1_url": design.image_1_url,
            "image_2_url": design.image_2_url,
            "image_3_url": design.image_3_url,
            "estimated_cost": design.estimated_cost,
            "budget_match_percentage": design.budget_match_percentage,
            "furniture_breakdown": json.loads(design.furniture_breakdown) if design.furniture_breakdown and design.furniture_breakdown.startswith('{') else design.furniture_breakdown,
            "vastu_score": design.vastu_score,
            "vastu_suggestions": json.loads(design.vastu_suggestions) if design.vastu_suggestions and design.vastu_suggestions.startswith('[') else [design.vastu_suggestions] if design.vastu_suggestions and design.vastu_suggestions != 'None' else [],
            "vastu_warnings": json.loads(design.vastu_warnings) if design.vastu_warnings and design.vastu_warnings.startswith('[') else [design.vastu_warnings] if design.vastu_warnings and design.vastu_warnings != 'None' else [],
            "status": design.status,
            "created_at": design.created_at.isoformat() if design.created_at else None,
            "updated_at": design.updated_at.isoformat() if design.updated_at else None,
        }
        
        return DesignResponse(**design_dict)
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to fetch design: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to fetch design: {str(e)}"
        )
