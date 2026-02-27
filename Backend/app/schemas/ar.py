"""
AR Schemas for API request/response models
"""

from pydantic import BaseModel
from typing import Optional, Dict, Any
from datetime import datetime


class ARSessionCreateRequest(BaseModel):
    """Schema for creating AR session."""
    room_id: str
    user_id: str
    design_id: Optional[str] = None


class ARSessionCreateResponse(BaseModel):
    """Schema for AR session creation response."""
    session_id: str
    room_id: str
    user_id: str
    design_id: Optional[str] = None
    created_at: datetime
    expires_at: datetime
    ar_config: Dict[str, Any]


class ARSessionStatusResponse(BaseModel):
    """Schema for AR session status response."""
    session_id: str
    status: str
    created_at: datetime
    updated_at: datetime
    ar_config: Dict[str, Any]


class ARSessionCompleteRequest(BaseModel):
    """Schema for completing AR session."""
    session_id: str
    user_feedback: Optional[Dict[str, Any]] = None
    session_data: Optional[Dict[str, Any]] = None


class ARSessionCompleteResponse(BaseModel):
    """Schema for AR session completion response."""
    session_id: str
    status: str
    completed_at: datetime
    user_feedback: Optional[Dict[str, Any]] = None


class ARModelRequest(BaseModel):
    """Schema for AR model requests."""
    model_name: str
    position: Optional[Dict[str, float]] = None
    rotation: Optional[Dict[str, float]] = None
    scale: Optional[float] = 1.0


class ARModelResponse(BaseModel):
    """Schema for AR model response."""
    model_url: str
    model_name: str
    ar_supported: bool
    loading_status: str


class ErrorResponse(BaseModel):
    """Schema for error responses."""
    error: str
    detail: Optional[str] = None
    status_code: int
