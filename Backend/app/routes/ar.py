"""
AR Session API routes for managing mobile AR visualization sessions.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import Dict, Any
import logging

from app.database import get_db
from app.schemas.ar import (
    ARSessionCreateRequest,
    ARSessionCreateResponse,
    ARSessionStatusResponse,
    ARSessionCompleteRequest,
    ARSessionCompleteResponse,
    ErrorResponse
)
from app.services.ar_service import ar_service
from app.dependencies import get_current_user_optional
from collections import defaultdict
from time import time

logger = logging.getLogger(__name__)

# Create router
router = APIRouter(prefix="/api/ar", tags=["AR Sessions"])

# Simple in-memory rate limiter for AR sessions (5 sessions per hour per user)
class SimpleRateLimiter:
    def __init__(self, max_requests: int, window_seconds: int):
        self.max_requests = max_requests
        self.window_seconds = window_seconds
        self.requests = defaultdict(list)
    
    def is_allowed(self, user_id: str) -> bool:
        now = time()
        user_requests = self.requests[user_id]
        
        # Remove old requests outside the window
        self.requests[user_id] = [req_time for req_time in user_requests if now - req_time < self.window_seconds]
        
        # Check if under limit
        if len(self.requests[user_id]) < self.max_requests:
            self.requests[user_id].append(now)
            return True
        
        return False

ar_rate_limiter = SimpleRateLimiter(max_requests=5, window_seconds=3600)


@router.post(
    "/session/create",
    response_model=ARSessionCreateResponse,
    responses={
        200: {"description": "AR session created successfully"},
        400: {"model": ErrorResponse, "description": "Invalid request"},
        429: {"model": ErrorResponse, "description": "Rate limit exceeded"},
        500: {"model": ErrorResponse, "description": "Internal server error"}
    }
)
async def create_ar_session(
    request: ARSessionCreateRequest,
    db: Session = Depends(get_db),
    current_user: Dict[str, Any] = Depends(get_current_user_optional)
):
    """
    Create a new AR session for mobile visualization.
    
    Generates a QR code that bridges desktop to mobile AR experience.
    Session expires after 15 minutes for security.
    """
    try:
        # Skip user authentication validation for testing
        # In production, uncomment this:
        # if not current_user or current_user.get('uid') != request.user_id:
        #     raise HTTPException(
        #         status_code=status.HTTP_401_UNAUTHORIZED,
        #         detail="Unauthorized access"
        #     )
        
        # Apply rate limiting
        user_id = request.user_id
        if not ar_rate_limiter.is_allowed(user_id):
            raise HTTPException(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                detail="Rate limit exceeded: Maximum 5 AR sessions per hour"
            )
        
        # Create AR session
        response = await ar_service.create_session(request, db)
        
        logger.info(f"AR session created: {response.session_id} for user {user_id}")
        return response
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Unexpected error creating AR session: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create AR session"
        )


@router.get(
    "/session/{session_id}",
    response_model=ARSessionStatusResponse,
    responses={
        200: {"description": "Session status retrieved successfully"},
        404: {"model": ErrorResponse, "description": "Session not found"},
        410: {"model": ErrorResponse, "description": "Session expired"},
        500: {"model": ErrorResponse, "description": "Internal server error"}
    }
)
async def get_session_status(
    session_id: str,
    db: Session = Depends(get_db)
):
    """
    Get AR session status for real-time polling.
    
    Used by desktop to check if mobile AR session is completed
    and retrieve screenshot when available.
    """
    try:
        response = await ar_service.get_session_status(session_id, db)
        return response
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Unexpected error getting session status: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve session status"
        )


@router.post(
    "/session/{session_id}/complete",
    response_model=ARSessionCompleteResponse,
    responses={
        200: {"description": "AR session completed successfully"},
        400: {"model": ErrorResponse, "description": "Invalid request"},
        404: {"model": ErrorResponse, "description": "Session not found"},
        410: {"model": ErrorResponse, "description": "Session expired"},
        500: {"model": ErrorResponse, "description": "Internal server error"}
    }
)
async def complete_ar_session(
    session_id: str,
    request: ARSessionCompleteRequest,
    db: Session = Depends(get_db)
):
    """
    Complete AR session with screenshot and placement data.
    
    Called by mobile AR experience when user completes visualization.
    Saves screenshot and updates session status.
    """
    try:
        # Validate session ID matches
        if request.session_id != session_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Session ID mismatch"
            )
        
        response = await ar_service.complete_session(request, db)
        
        logger.info(f"AR session completed: {session_id}")
        return response
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Unexpected error completing AR session: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to complete AR session"
        )


@router.delete(
    "/session/{session_id}",
    responses={
        200: {"description": "Session deleted successfully"},
        404: {"model": ErrorResponse, "description": "Session not found"},
        500: {"model": ErrorResponse, "description": "Internal server error"}
    }
)
async def delete_ar_session(
    session_id: str,
    db: Session = Depends(get_db),
    current_user: Dict[str, Any] = Depends(get_current_user_optional)
):
    """
    Delete an AR session (admin/user cleanup).
    
    Allows users to delete their own AR sessions.
    """
    try:
        from app.models.ar_session import ARSession
        
        # Get session
        ar_session = db.query(ARSession).filter(
            ARSession.id == session_id
        ).first()
        
        if not ar_session:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="AR session not found"
            )
        
        # Validate ownership
        if not current_user or current_user.get('uid') != ar_session.user_id:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Unauthorized access"
            )
        
        # Delete session
        db.delete(ar_session)
        db.commit()
        
        logger.info(f"AR session deleted: {session_id}")
        return {"success": True, "message": "AR session deleted successfully"}
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Unexpected error deleting AR session: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to delete AR session"
        )


@router.get(
    "/sessions/user/{user_id}",
    responses={
        200: {"description": "User sessions retrieved successfully"},
        401: {"model": ErrorResponse, "description": "Unauthorized access"},
        500: {"model": ErrorResponse, "description": "Internal server error"}
    }
)
async def get_user_sessions(
    user_id: str,
    limit: int = 10,
    db: Session = Depends(get_db),
    current_user: Dict[str, Any] = Depends(get_current_user_optional)
):
    """
    Get AR sessions for a specific user.
    
    Returns user's AR sessions with pagination.
    """
    try:
        from app.models.ar_session import ARSession
        
        # Validate ownership
        if not current_user or current_user.get('uid') != user_id:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Unauthorized access"
            )
        
        # Get user sessions
        sessions = db.query(ARSession).filter(
            ARSession.user_id == user_id
        ).order_by(ARSession.created_at.desc()).limit(limit).all()
        
        return {
            "success": True,
            "sessions": [session.to_dict() for session in sessions],
            "total": len(sessions)
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Unexpected error getting user sessions: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve user sessions"
        )
