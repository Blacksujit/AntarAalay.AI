from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime


class RoomCreate(BaseModel):
    room_type: Optional[str] = None
    direction: Optional[str] = None


class RoomResponse(BaseModel):
    id: str
    user_id: str
    image_url: str
    room_type: Optional[str]
    direction: Optional[str]
    created_at: datetime

    class Config:
        from_attributes = True


class RoomUploadResponse(BaseModel):
    room_id: str
    image_url: str
    message: str
