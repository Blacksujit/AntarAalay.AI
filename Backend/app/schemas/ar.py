"""
AR session request and response schemas for API validation.
"""

from pydantic import BaseModel, Field, validator
from typing import Optional, Dict, Any
from datetime import datetime
from enum import Enum


class ARSessionStatus(str, Enum):
    """AR Session status enumeration."""
    PENDING = "pending"
    ACTIVE = "active"
    COMPLETED = "completed"
    EXPIRED = "expired"


class ARSessionCreateRequest(BaseModel):
    """Request schema for creating AR session."""
    user_id: str = Field(..., description="User ID (Firebase UID)")
    design_id: str = Field(..., description="Design ID to visualize in AR")
    room_id: str = Field(..., description="Room ID associated with the design")
    
    @validator('user_id', 'design_id', 'room_id')
    def validate_ids(cls, v):
        """Validate that IDs are not empty."""
        if not v or not v.strip():
            raise ValueError("ID cannot be empty")
        return v.strip()
    
    class Config:
        schema_extra = {
            "example": {
                "user_id": "firebase-uid-123",
                "design_id": "design-uuid-456",
                "room_id": "room-uuid-789"
            }
        }


class ARSessionCreateResponse(BaseModel):
    """Response schema for AR session creation."""
    success: bool = Field(..., description="Session creation success status")
    session_id: str = Field(..., description="AR session ID")
    mobile_url: str = Field(..., description="Mobile AR session URL")
    qr_code_data: str = Field(..., description="QR code data")
    expires_at: datetime = Field(..., description="Session expiration time")
    
    class Config:
        schema_extra = {
            "example": {
                "success": True,
                "session_id": "session-uuid-123",
                "mobile_url": "https://domain.com/ar/session-uuid-123",
                "qr_code_data": "https://domain.com/ar/session-uuid-123",
                "expires_at": "2024-01-01T12:15:00Z"
            }
        }


class ARSessionStatusResponse(BaseModel):
    """Response schema for AR session status."""
    success: bool = Field(..., description="Status check success")
    session_id: str = Field(..., description="AR session ID")
    status: ARSessionStatus = Field(..., description="Current session status")
    screenshot_url: Optional[str] = Field(None, description="AR session screenshot URL")
    expires_at: datetime = Field(..., description="Session expiration time")
    created_at: datetime = Field(..., description="Session creation time")
    
    class Config:
        schema_extra = {
            "example": {
                "success": True,
                "session_id": "session-uuid-123",
                "status": "completed",
                "screenshot_url": "https://cdn.domain.com/ar-screenshots/123.jpg",
                "expires_at": "2024-01-01T12:15:00Z",
                "created_at": "2024-01-01T12:00:00Z"
            }
        }


class ARSessionCompleteRequest(BaseModel):
    """Request schema for completing AR session."""
    session_id: str = Field(..., description="AR session ID")
    screenshot_data: str = Field(..., description="Base64 encoded screenshot")
    anchor_transform: Optional[Dict[str, Any]] = Field(None, description="Anchor transform data")
    
    @validator('screenshot_data')
    def validate_screenshot(cls, v):
        """Validate screenshot data format."""
        if not v.startswith('data:image/'):
            raise ValueError("Screenshot must be a base64 encoded image")
        return v
    
    class Config:
        schema_extra = {
            "example": {
                "session_id": "session-uuid-123",
                "screenshot_data": "data:image/jpeg;base64,/9j/4AAQSkZJRgABAQAAAQ...",
                "anchor_transform": {
                    "position": {"x": 0, "y": 0, "z": 0},
                    "rotation": {"x": 0, "y": 0, "z": 0, "w": 1},
                    "scale": {"x": 1, "y": 1, "z": 1}
                }
            }
        }


class ARSessionCompleteResponse(BaseModel):
    """Response schema for AR session completion."""
    success: bool = Field(..., description="Completion success status")
    message: str = Field(..., description="Completion message")
    session_id: str = Field(..., description="AR session ID")
    screenshot_url: Optional[str] = Field(None, description="Saved screenshot URL")
    
    class Config:
        schema_extra = {
            "example": {
                "success": True,
                "message": "AR session completed successfully",
                "session_id": "session-uuid-123",
                "screenshot_url": "https://cdn.domain.com/ar-screenshots/123.jpg"
            }
        }


class ErrorResponse(BaseModel):
    """Standard error response schema."""
    success: bool = Field(False, description="Error status")
    error: str = Field(..., description="Error message")
    code: Optional[str] = Field(None, description="Error code")
    
    class Config:
        schema_extra = {
            "example": {
                "success": False,
                "error": "Session not found or expired",
                "code": "SESSION_NOT_FOUND"
            }
        }
