from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File, Form
from sqlalchemy.orm import Session
from typing import Optional
import uuid

from app.database import get_db
from app.dependencies import get_current_user
from app.services.storage import get_storage_service
from app.schemas.room import RoomUploadResponse, RoomResponse
from app.models.room import Room as RoomModel
from app.models.user import User as UserModel
from app.config import get_settings

router = APIRouter(prefix="/api/room", tags=["room"])
settings = get_settings()


@router.post("/upload", response_model=RoomUploadResponse)
async def upload_room_image(
    file: UploadFile = File(...),
    room_type: Optional[str] = Form(None),
    direction: Optional[str] = Form(None),
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """
    Upload a room image to S3 and create a room record
    """
    # Validate file type
    if file.content_type not in settings.allowed_image_types_list:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid file type. Allowed types: {', '.join(settings.allowed_image_types_list)}"
        )
    
    # Read file content
    content = await file.read()
    
    # Validate file size
    if len(content) > settings.MAX_UPLOAD_SIZE:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"File too large. Maximum size: {settings.MAX_UPLOAD_SIZE / (1024 * 1024):.1f}MB"
        )
    
    try:
        # Upload to S3
        image_url = get_storage_service().upload_image(content, file.content_type, "rooms")
        
        # Create room record
        room_id = str(uuid.uuid4())
        room = RoomModel(
            id=room_id,
            user_id=current_user["uid"],
            image_url=image_url,
            room_type=room_type,
            direction=direction
        )
        
        # Ensure user exists in DB
        user = db.query(UserModel).filter(UserModel.id == current_user["uid"]).first()
        if not user:
            user = UserModel(
                id=current_user["uid"],
                email=current_user["email"],
                name=current_user.get("name"),
                photo_url=current_user.get("photo_url")
            )
            db.add(user)
        
        db.add(room)
        db.commit()
        db.refresh(room)
        
        return RoomUploadResponse(
            room_id=room.id,
            image_url=room.image_url,
            message="Room image uploaded successfully"
        )
        
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to upload image: {str(e)}"
        )


@router.get("/{room_id}", response_model=RoomResponse)
async def get_room(
    room_id: str,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """
    Get room details by ID
    """
    room = db.query(RoomModel).filter(
        RoomModel.id == room_id,
        RoomModel.user_id == current_user["uid"]
    ).first()
    
    if not room:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Room not found"
        )
    
    return room


@router.get("/user/rooms")
async def get_user_rooms(
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """
    Get all rooms for the current user
    """
    rooms = db.query(RoomModel).filter(
        RoomModel.user_id == current_user["uid"]
    ).order_by(RoomModel.created_at.desc()).all()
    
    return {"rooms": rooms, "total": len(rooms)}
