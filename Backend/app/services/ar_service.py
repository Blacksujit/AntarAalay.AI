"""
AR Session service for managing mobile AR visualization sessions.
"""

import uuid
import base64
import os
from datetime import datetime, timedelta
from typing import Optional, Dict, Any
from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from app.models.ar_session import ARSession, ARSessionStatus
from app.schemas.ar import (
    ARSessionCreateRequest, 
    ARSessionCreateResponse,
    ARSessionStatusResponse,
    ARSessionCompleteRequest,
    ARSessionCompleteResponse
)
from app.services.storage import get_storage_service
import logging

logger = logging.getLogger(__name__)


class ARService:
    """
    Service for managing AR visualization sessions.
    
    Handles QR-based bridge between desktop and mobile AR experiences
    with production-grade session management and security.
    """
    
    def __init__(self):
        """Initialize AR service with storage service."""
        self.storage_service = get_storage_service()
        self.base_url = os.getenv("AR_BASE_URL", "https://antaralay-ar.vercel.app")
        self.session_timeout_minutes = int(os.getenv("AR_SESSION_TIMEOUT_MINUTES", "60"))
        
    async def create_session(
        self, 
        request: ARSessionCreateRequest,
        db: Session
    ) -> ARSessionCreateResponse:
        """
        Create a new AR session for mobile visualization.
        
        Args:
            request: AR session creation request
            db: Database session
            
        Returns:
            AR session creation response with QR code data
            
        Raises:
            HTTPException: If session creation fails
        """
        try:
            # Generate unique session ID
            session_id = str(uuid.uuid4())
            
            # Create mobile URL
            mobile_url = f"{self.base_url}/ar/{session_id}"
            
            # Calculate expiration time
            expires_at = datetime.utcnow() + timedelta(minutes=self.session_timeout_minutes)
            
            # Create session record
            ar_session = ARSession(
                id=session_id,
                user_id=request.user_id,
                design_id=request.design_id,
                room_id=request.room_id,
                status=ARSessionStatus.PENDING,
                mobile_url=mobile_url,
                expires_at=expires_at
            )
            
            # Save to database
            db.add(ar_session)
            db.commit()
            db.refresh(ar_session)
            
            logger.info(f"Created AR session {session_id} for user {request.user_id}")
            
            return ARSessionCreateResponse(
                success=True,
                session_id=session_id,
                mobile_url=mobile_url,
                qr_code_data=mobile_url,
                expires_at=expires_at
            )
            
        except Exception as e:
            logger.error(f"Failed to create AR session: {str(e)}")
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to create AR session"
            )
    
    async def get_session_status(
        self, 
        session_id: str,
        db: Session
    ) -> ARSessionStatusResponse:
        """
        Get AR session status for polling.
        
        Args:
            session_id: AR session ID
            db: Database session
            
        Returns:
            Current session status
            
        Raises:
            HTTPException: If session not found or expired
        """
        try:
            # Get session from database
            ar_session = db.query(ARSession).filter(
                ARSession.id == session_id
            ).first()
            
            if not ar_session:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="AR session not found"
                )
            
            # Check if session has expired
            if ar_session.is_expired() and ar_session.status != ARSessionStatus.COMPLETED:
                ar_session.status = ARSessionStatus.EXPIRED
                db.commit()
                raise HTTPException(
                    status_code=status.HTTP_410_GONE,
                    detail="AR session has expired"
                )
            
            logger.info(f"Retrieved AR session {session_id} with status {ar_session.status}")
            
            return ARSessionStatusResponse(
                success=True,
                session_id=session_id,
                status=ar_session.status,
                screenshot_url=ar_session.screenshot_url,
                expires_at=ar_session.expires_at,
                created_at=ar_session.created_at
            )
            
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Failed to get AR session status: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to retrieve session status"
            )
    
    async def complete_session(
        self,
        request: ARSessionCompleteRequest,
        db: Session
    ) -> ARSessionCompleteResponse:
        """
        Complete AR session with screenshot and placement data.
        
        Args:
            request: AR session completion request
            db: Database session
            
        Returns:
            Completion response with screenshot URL
            
        Raises:
            HTTPException: If session not found or invalid
        """
        try:
            # Get session from database
            ar_session = db.query(ARSession).filter(
                ARSession.id == request.session_id
            ).first()
            
            if not ar_session:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="AR session not found"
                )
            
            # Check if session has expired
            if ar_session.is_expired():
                raise HTTPException(
                    status_code=status.HTTP_410_GONE,
                    detail="AR session has expired"
                )
            
            # Process and save screenshot
            screenshot_url = await self._save_screenshot(
                request.session_id,
                request.screenshot_data,
                ar_session.user_id
            )
            
            # Update session with completion data
            ar_session.status = ARSessionStatus.COMPLETED
            ar_session.screenshot_url = screenshot_url
            if request.anchor_transform:
                ar_session.anchor_transform = str(request.anchor_transform)
            ar_session.updated_at = datetime.utcnow()
            
            db.commit()
            db.refresh(ar_session)
            
            logger.info(f"Completed AR session {request.session_id} with screenshot")
            
            return ARSessionCompleteResponse(
                success=True,
                message="AR session completed successfully",
                session_id=request.session_id,
                screenshot_url=screenshot_url
            )
            
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Failed to complete AR session: {str(e)}")
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to complete AR session"
            )
    
    async def _save_screenshot(
        self, 
        session_id: str, 
        screenshot_data: str, 
        user_id: str
    ) -> str:
        """
        Save AR session screenshot to storage.
        
        Args:
            session_id: AR session ID
            screenshot_data: Base64 encoded image data
            user_id: User ID for storage path
            
        Returns:
            Public URL of saved screenshot
        """
        try:
            # Extract base64 data
            image_data = base64.b64decode(screenshot_data.split(',')[1])
            
            # Generate filename
            timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
            filename = f"ar_screenshots/{user_id}/{session_id}_{timestamp}.jpg"
            
            # Upload to storage
            screenshot_url = await self.storage_service.upload_bytes(
                data=image_data,
                filename=filename,
                content_type="image/jpeg"
            )
            
            return screenshot_url
            
        except Exception as e:
            logger.error(f"Failed to save AR screenshot: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to save AR screenshot"
            )
    
    async def cleanup_expired_sessions(self, db: Session) -> int:
        """
        Clean up expired AR sessions.
        
        Args:
            db: Database session
            
        Returns:
            Number of sessions cleaned up
        """
        try:
            # Update expired sessions to expired status
            expired_count = db.query(ARSession).filter(
                ARSession.expires_at < datetime.utcnow(),
                ARSession.status.in_([ARSessionStatus.PENDING, ARSessionStatus.ACTIVE])
            ).update(
                {ARSession.status: ARSessionStatus.EXPIRED},
                synchronize_session=False
            )
            
            db.commit()
            
            if expired_count > 0:
                logger.info(f"Marked {expired_count} AR sessions as expired")
            
            return expired_count
            
        except Exception as e:
            logger.error(f"Failed to cleanup expired sessions: {str(e)}")
            db.rollback()
            return 0


# Global AR service instance
ar_service = ARService()
