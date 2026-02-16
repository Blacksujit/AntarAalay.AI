"""
Room Upload API Routes
POST /api/room/upload
"""
from fastapi import APIRouter, Depends, UploadFile, File, HTTPException, status
from typing import Dict
from app.dependencies import get_current_user
from app.services.room_service import room_upload_service

router = APIRouter(prefix="/room", tags=["room"])


@router.post("/upload", response_model=Dict)
async def upload_room_images(
    north: UploadFile = File(..., description="North facing image"),
    south: UploadFile = File(..., description="South facing image"),
    east: UploadFile = File(..., description="East facing image"),
    west: UploadFile = File(..., description="West facing image"),
    current_user: dict = Depends(get_current_user)
):
    """
    Upload 4 directional room images (North, South, East, West).
    
    - **north**: North facing image (JPEG/PNG/WebP, max 10MB)
    - **south**: South facing image (JPEG/PNG/WebP, max 10MB)
    - **east**: East facing image (JPEG/PNG/WebP, max 10MB)
    - **west**: West facing image (JPEG/PNG/WebP, max 10MB)
    
    Returns room_id and image URLs.
    """
    try:
        user_id = current_user.get('localId') or current_user.get('user_id')
        
        if not user_id:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User ID not found in token"
            )
        
        result = await room_upload_service.upload_room_images(
            user_id=user_id,
            north=north,
            south=south,
            east=east,
            west=west
        )
        
        return result
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Upload failed: {str(e)}"
        )


@router.get("/user/rooms")
async def get_user_rooms(current_user: dict = Depends(get_current_user)):
    """Get all rooms for the current user."""
    user_id = current_user.get('localId') or current_user.get('user_id')
    rooms = await room_upload_service.get_user_rooms(user_id)
    return {"rooms": rooms, "total": len(rooms)}


@router.get("/{room_id}")
async def get_room(room_id: str, current_user: dict = Depends(get_current_user)):
    """Get a specific room by ID."""
    user_id = current_user.get('localId') or current_user.get('user_id')
    room = await room_upload_service.get_room(room_id, user_id)
    
    if not room:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Room not found"
        )
    
    return room
