"""
Room Service for AntarAalay.ai

Handles 4-directional image uploads to Firebase Storage
and room metadata storage in Firestore.
"""
import uuid
from datetime import datetime
from typing import Dict, Optional, List
from fastapi import UploadFile, HTTPException, status

from app.config import get_settings
from app.services.firebase_client import get_firestore, get_storage_bucket
import logging

logger = logging.getLogger(__name__)


class RoomUploadService:
    """Service for handling room image uploads with Firebase."""
    
    def __init__(self):
        self.settings = get_settings()
        self.firestore = get_firestore()
        self.storage_bucket = get_storage_bucket()
    
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
                
                # Upload to Firebase Storage
                path = f"users/{user_id}/rooms/{room_id}/{direction}.jpg"
                blob = self.storage_bucket.blob(path)
                blob.upload_from_string(
                    content,
                    content_type=file.content_type or "image/jpeg"
                )
                
                # Make publicly accessible
                blob.make_public()
                images[direction] = blob.public_url
                
                logger.info(f"Uploaded {direction} image: {blob.public_url}")
            
            # Save to Firestore
            self.firestore.collection('rooms').document(room_id).set({
                'room_id': room_id,
                'user_id': user_id,
                'images': images,
                'created_at': datetime.utcnow().isoformat(),
                'updated_at': datetime.utcnow().isoformat()
            })
            
            logger.info(f"Room {room_id} saved to Firestore")
            
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
            doc_ref = self.firestore.collection('rooms').document(room_id)
            doc = doc_ref.get()
            
            if not doc.exists:
                return None
            
            room_data = doc.to_dict()
            
            # Verify ownership
            if room_data.get('user_id') != user_id:
                return None
            
            return room_data
            
        except Exception as e:
            logger.error(f"Error fetching room {room_id}: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to fetch room"
            )
    
    async def get_user_rooms(self, user_id: str) -> List[Dict]:
        """Get all rooms for a user."""
        try:
            docs = self.firestore.collection('rooms').where('user_id', '==', user_id).stream()
            return [doc.to_dict() for doc in docs]
        except Exception as e:
            logger.error(f"Error fetching rooms for user {user_id}: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to fetch rooms"
            )


room_upload_service = RoomUploadService()
