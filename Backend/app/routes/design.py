"""
Design API Routes for AntarAalay.ai

Endpoints for:
- Generating AI designs with Stability AI
- Regenerating with customizations
- Fetching design history
"""
from fastapi import APIRouter, Depends, HTTPException, status
from typing import List, Optional
import uuid

from app.dependencies import get_current_user
from app.schemas.design import (
    DesignGenerateRequest,
    DesignGenerateResponse,
    DesignResponse,
    DesignListResponse,
    DesignCustomizationRequest
)
from app.services.stability_engine import (
    get_stability_engine,
    CustomizationOptions,
    GenerationResult
)
from app.services.firebase_client import get_firestore, get_firebase_storage
from app.services.room_service import room_upload_service
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/design", tags=["design"])


@router.post("/generate", response_model=DesignGenerateResponse)
async def generate_design(
    request: DesignGenerateRequest,
    current_user: dict = Depends(get_current_user)
):
    """
    Generate AI interior designs from room images.
    
    - Fetches room from Firestore
    - Uses Stability AI for image-to-image generation
    - Saves design to Firestore
    - Returns 3 design variations
    """
    try:
        user_id = current_user.get('uid') or current_user.get('localId')
        
        # Get room data
        room = await room_upload_service.get_room(request.room_id, user_id)
        if not room:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Room not found"
            )
        
        # Use north image as base (primary direction)
        base_image_url = room['images'].get('north')
        if not base_image_url:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Room missing north image"
            )
        
        # Prepare customization (minimal for MVP; schema currently supports style/budget only)
        customization = CustomizationOptions(style=request.style)
        
        # Generate designs with Stability AI
        stability = get_stability_engine()
        result: GenerationResult = await stability.generate_designs(
            base_image_url=base_image_url,
            customization=customization,
            num_variations=3
        )
        
        if not result.success:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"AI generation failed: {result.error_message}"
            )
        
        # Save design to Firestore
        design_id = str(uuid.uuid4())
        firestore = get_firestore()
        
        design_data = await firestore.create_design(
            design_id=design_id,
            room_id=request.room_id,
            user_id=user_id,
            style=request.style,
            customization={},
            prompt_used=result.prompt_used,
            generated_images=result.image_urls,
            version=1
        )
        
        logger.info(f"Design generated: {design_id} for room {request.room_id}")
        
        return DesignGenerateResponse(
            design_id=design_id,
            status="completed",
            message="Design generated successfully"
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Design generation failed: {e}")
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
    
    - Fetches original room images
    - Merges previous and new customizations
    - Generates new variations
    - Saves as new design version
    """
    try:
        user_id = current_user.get('uid') or current_user.get('localId')
        
        # Get original design
        firestore = get_firestore()
        original_design = await firestore.get_design(design_id, user_id)
        
        if not original_design:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Design not found"
            )
        
        # Get room for base image
        room_id = original_design['room_id']
        room = await room_upload_service.get_room(room_id, user_id)
        
        if not room:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Room not found"
            )
        
        base_image_url = room['images'].get('north')
        if not base_image_url:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Room missing base image"
            )
        
        # Merge customizations
        prev_custom = original_design.get('customization', {})
        new_custom = {
            'wall_color': request.wall_color or prev_custom.get('wall_color'),
            'flooring': request.flooring or prev_custom.get('flooring'),
            'furniture_style': request.furniture_style or prev_custom.get('furniture_style')
        }
        
        # Generate with new customization
        prev_options = CustomizationOptions(
            wall_color=prev_custom.get('wall_color'),
            flooring=prev_custom.get('flooring'),
            furniture_style=prev_custom.get('furniture_style'),
            style=original_design.get('style', 'modern')
        )
        
        new_options = CustomizationOptions(
            wall_color=request.wall_color,
            flooring=request.flooring,
            furniture_style=request.furniture_style,
            style=request.style
        )
        
        stability = get_stability_engine()
        result = await stability.regenerate_with_changes(
            base_image_url=base_image_url,
            previous_customization=prev_options,
            new_customization=new_options,
            num_variations=3
        )
        
        if not result.success:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Regeneration failed: {result.error_message}"
            )
        
        # Save as new design
        new_design_id = str(uuid.uuid4())
        new_version = original_design.get('version', 1) + 1
        
        design_data = await firestore.create_design(
            design_id=new_design_id,
            room_id=room_id,
            user_id=user_id,
            style=request.style or original_design.get('style', 'modern'),
            customization=new_custom,
            prompt_used=result.prompt_used,
            generated_images=result.image_urls,
            version=new_version
        )
        
        logger.info(f"Design regenerated: {new_design_id} (v{new_version}) from {design_id}")
        
        return DesignResponse(**design_data)
        
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

        firestore = get_firestore()
        designs = await firestore.get_room_designs(room_id, user_id)

        room_image_url = (room.get("images") or {}).get("north")
        room_payload = {
            "id": room.get("room_id") or room_id,
            "image_url": room_image_url,
            "room_type": room.get("room_type"),
            "direction": room.get("direction"),
        }

        designs_payload = []
        for d in designs:
            design_obj = DesignResponse(**d)
            designs_payload.append(
                {
                    "design": design_obj.model_dump(),
                    "room_image_url": room_image_url,
                    "budget_summary": None,
                }
            )

        return {
            "designs": designs_payload,
            "total": len(designs_payload),
            "room": room_payload,
        }
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
    current_user: dict = Depends(get_current_user)
):
    """
    Get a specific design by ID.
    """
    try:
        user_id = current_user.get('uid') or current_user.get('localId')
        
        firestore = get_firestore()
        design = await firestore.get_design(design_id, user_id)
        
        if not design:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Design not found"
            )
        
        return DesignResponse(**design)
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to fetch design: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to fetch design: {str(e)}"
        )
