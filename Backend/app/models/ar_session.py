"""
AR Session model for managing mobile AR visualization sessions.
"""

from sqlalchemy import Column, String, DateTime, Enum, Text, Index
from sqlalchemy.sql import func
from datetime import datetime, timedelta
from enum import Enum as PyEnum
import uuid

from app.database import Base


class ARSessionStatus(PyEnum):
    """AR Session status enumeration."""
    PENDING = "pending"
    ACTIVE = "active"
    COMPLETED = "completed"
    EXPIRED = "expired"


class ARSession(Base):
    """
    AR Session model for managing mobile AR visualization sessions.
    
    Handles QR-based bridge between desktop and mobile AR experiences
    with Vastu-aligned furniture placement.
    """
    __tablename__ = "ar_sessions"
    __allow_unmapped__ = True  # SQLAlchemy 2.0 compatibility
    
    # Primary Key
    id = Column(
        String(36), 
        primary_key=True, 
        index=True,
        default=lambda: str(uuid.uuid4()),
        comment="UUID session identifier"
    )
    
    # Foreign Keys
    user_id = Column(
        String(128),
        nullable=False,
        index=True,
        comment="Owner user ID (Firebase UID)"
    )
    design_id = Column(
        String(36),
        nullable=False,
        index=True,
        comment="Associated design ID"
    )
    room_id = Column(
        String(36),
        nullable=False,
        index=True,
        comment="Associated room ID"
    )
    
    # Session Status
    status = Column(
        Enum(ARSessionStatus),
        default=ARSessionStatus.PENDING,
        nullable=False,
        comment="Current session status"
    )
    
    # URLs and Data
    mobile_url = Column(
        String(512),
        nullable=True,
        comment="Mobile AR session URL"
    )
    screenshot_url = Column(
        String(512),
        nullable=True,
        comment="AR session screenshot URL"
    )
    anchor_transform = Column(
        Text,
        nullable=True,
        comment="JSON-encoded anchor transform data"
    )
    
    # Timestamps
    created_at = Column(
        DateTime,
        default=func.now(),
        nullable=False,
        comment="Session creation timestamp"
    )
    expires_at = Column(
        DateTime,
        default=lambda: datetime.utcnow() + timedelta(minutes=15),
        nullable=False,
        comment="Session expiration timestamp"
    )
    updated_at = Column(
        DateTime,
        default=func.now(),
        onupdate=func.now(),
        nullable=False,
        comment="Last update timestamp"
    )
    
    # Indexes for performance
    __table_args__ = (
        Index('idx_user_sessions', 'user_id', 'created_at'),
        Index('idx_session_expires', 'expires_at'),
        Index('idx_design_sessions', 'design_id'),
    )
    
    def __repr__(self):
        return f"<ARSession(id={self.id}, user_id={self.user_id}, status={self.status})>"
    
    def is_expired(self) -> bool:
        """Check if session has expired."""
        return datetime.utcnow() > self.expires_at
    
    def to_dict(self) -> dict:
        """Convert session to dictionary representation."""
        return {
            'id': self.id,
            'user_id': self.user_id,
            'design_id': self.design_id,
            'room_id': self.room_id,
            'status': self.status.value if self.status else None,
            'mobile_url': self.mobile_url,
            'screenshot_url': self.screenshot_url,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'expires_at': self.expires_at.isoformat() if self.expires_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
