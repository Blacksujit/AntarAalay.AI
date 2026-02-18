"""
Room Service for AntarAalay.ai

Handles 4-directional image uploads to local storage
and room metadata storage in database.
"""
import uuid
from datetime import datetime
from typing import Dict, Optional, List
from fastapi import UploadFile, HTTPException, status

from app.config import get_settings
from app.services.storage import get_storage_service
import logging

logger = logging.getLogger(__name__)


class RoomUploadService:
    """Service for handling room image uploads with local storage."""
    
    def __init__(self):
        self.settings = get_settings()
        self.storage_service = get_storage_service()
    
    async def _validate_and_read(self, file: UploadFile, direction: str) -> bytes:
        """Validate and read image file."""
        allowed_types = self.settings.allowed_image_types_list
        if file.content_type not in allowed_types:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"{direction}: Invalid file type '{file.content_type}'. Allowed: {', '.join(allowed_types)}"
            )
        
        content = await file.read()
        
        if len(content) > self.settings.MAX_UPLOAD_SIZE:
            raise HTTPException(
                status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
                detail=f"{direction}: File too large. Max: {self.settings.MAX_UPLOAD_SIZE // (1024*1024)}MB"
            )
        
        await file.seek(0)
        return content
    
    async def upload_room_images(
        self,
        user_id: str,
        north: UploadFile,
        south: UploadFile,
        east: UploadFile,
        west: UploadFile
    ) -> Dict:
        """Upload 4 directional room images."""
        try:
            room_id = str(uuid.uuid4())
            folder = f"users/{user_id}/rooms/{room_id}"
            
            logger.info(f"Starting room upload for user {user_id}, room {room_id}")
            
            images = {}
            directions = {"north": north, "south": south, "east": east, "west": west}
            
            for direction, file in directions.items():
                content = await self._validate_and_read(file, direction)
                
                # Upload to local storage
                folder = f"users/{user_id}/rooms/{room_id}"
                image_url = self.storage_service.upload_image(
                    content,
                    file.content_type or "image/jpeg",
                    folder
                )
                
                images[direction] = image_url
                logger.info(f"Uploaded {direction} image: {image_url}")
            
            # Save to database (using SQLite for now instead of Firestore)
            from app.database import get_db_manager
            
            db_manager = get_db_manager()
            with db_manager.session_scope() as session:
                from app.models import Room
                # Create 4 separate room records, one for each direction
                for direction, image_url in images.items():
                    room = Room(
                        id=f"{room_id}_{direction}",  # Use 'id' field for primary key
                        user_id=user_id,
                        image_url=image_url,
                        room_type="living",  # Default room type
                        direction=direction,  # Store the direction
                        created_at=datetime.utcnow(),
                        updated_at=datetime.utcnow()
                    )
                    session.add(room)
                session.commit()
            
            logger.info(f"Room {room_id} with 4 directions saved to database")
            
            return {
                "room_id": room_id,
                "images": images,
                "status": "success"
            }
            
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Room upload failed: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Upload failed: {str(e)}"
            )
    
    async def get_room(self, room_id: str, user_id: str) -> Optional[Dict]:
        """Get room by ID with user verification."""
        try:
            # Get from SQLite database instead of Firestore
            from app.database import get_db_manager
            
            db_manager = get_db_manager()
            with db_manager.session_scope() as session:
                from app.models import Room
                # Find all room records with this room_id base (could have multiple directions)
                rooms = session.query(Room).filter(Room.id.like(f"{room_id}%")).all()
                
                if not rooms:
                    return None
                
                # Group by direction
                images = {}
                for room in rooms:
                    if room.direction:
                        images[room.direction] = room.image_url
                
                return {
                    'room_id': room_id,
                    'user_id': user_id,
                    'images': images,
                    'created_at': rooms[0].created_at.isoformat() if rooms[0].created_at else None,
                    'updated_at': rooms[0].updated_at.isoformat() if rooms[0].updated_at else None
                }
            
        except Exception as e:
            logger.error(f"Error fetching room {room_id}: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to fetch room: {str(e)}"
            )
    
    async def get_user_rooms(self, user_id: str) -> List[Dict]:
        """Get all rooms for a user."""
        try:
            # Get from SQLite database instead of Firestore
            from app.database import get_db_manager
            
            db_manager = get_db_manager()
            with db_manager.session_scope() as session:
                from app.models import Room
                from sqlalchemy import func
                
                # Group rooms by base room_id (without direction suffix)
                rooms = session.query(
                    func.substr(Room.id, 1, 36).label('base_room_id'),
                    Room.user_id,
                    Room.created_at,
                    Room.updated_at
                ).filter(Room.user_id == user_id).group_by('base_room_id').all()
                
                result = []
                for room in rooms:
                    # Get all directions for this room
                    direction_rooms = session.query(Room).filter(
                        Room.id.like(f"{room.base_room_id}%")
                    ).all()
                    
                    images = {}
                    for dr in direction_rooms:
                        if dr.direction:
                            images[dr.direction] = dr.image_url
                    
                    result.append({
                        'room_id': room.base_room_id,
                        'user_id': room.user_id,
                        'images': images,
                        'created_at': room.created_at.isoformat() if room.created_at else None,
                        'updated_at': room.updated_at.isoformat() if room.updated_at else None
                    })
                
                return result
                
        except Exception as e:
            logger.error(f"Error fetching rooms for user {user_id}: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to fetch user rooms: {str(e)}"
            )


room_upload_service = RoomUploadService()
