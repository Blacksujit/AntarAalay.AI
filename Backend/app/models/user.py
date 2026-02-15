"""
Module 3: Domain Models - User

User model representing authenticated users from Firebase.

Dependencies: Module 2 (Database - Base)
"""
from typing import TYPE_CHECKING, List, Optional
from sqlalchemy import Column, String, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from app.database import Base

# Type checking only imports to avoid circular dependencies
if TYPE_CHECKING:
    from app.models.room import Room
    from app.models.design import Design


class User(Base):
    """
    User model representing a Firebase-authenticated user.
    """
    __tablename__ = "users"
    __allow_unmapped__ = True  # SQLAlchemy 2.0 compatibility
    
    # Primary Key - Firebase UID
    id = Column(String(128), primary_key=True, index=True, comment="Firebase UID")
    
    # Profile Information
    email = Column(String(255), unique=True, index=True, nullable=False)
    name = Column(String(255), nullable=True)
    photo_url = Column(String(512), nullable=True)
    
    # Timestamps
    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
        comment="Record creation timestamp"
    )
    updated_at = Column(
        DateTime(timezone=True),
        onupdate=func.now(),
        nullable=True,
        comment="Last update timestamp"
    )
    
    # Relationships
    rooms: List["Room"] = relationship(
        "Room",
        back_populates="user",
        cascade="all, delete-orphan",
        lazy="dynamic"
    )
    
    designs: List["Design"] = relationship(
        "Design",
        back_populates="user",
        cascade="all, delete-orphan",
        lazy="dynamic"
    )
    
    def __repr__(self) -> str:
        """String representation of User."""
        return f"<User(id={self.id}, email={self.email})>"
    
    def __str__(self) -> str:
        """Human-readable string representation."""
        return f"{self.name or 'Unknown'} ({self.email})"
    
    @property
    def display_name(self) -> str:
        """Return display name or email if name not set."""
        return self.name or self.email.split('@')[0] if self.email else "Unknown"
    
    @property
    def room_count(self) -> int:
        """Return number of rooms owned by user."""
        return len(self.rooms) if self.rooms else 0
    
    @property
    def design_count(self) -> int:
        """Return number of designs owned by user."""
        return len(self.designs) if self.designs else 0
    
    def to_dict(self, include_relations: bool = False) -> dict:
        """
        Convert user to dictionary.
        
        Args:
            include_relations: Whether to include room/design IDs
            
        Returns:
            dict: User data as dictionary
        """
        data = {
            "id": self.id,
            "email": self.email,
            "name": self.name,
            "photo_url": self.photo_url,
            "display_name": self.display_name,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }
        
        if include_relations:
            data["room_ids"] = [r.id for r in self.rooms] if self.rooms else []
            data["design_ids"] = [d.id for d in self.designs] if self.designs else []
            data["room_count"] = self.room_count
            data["design_count"] = self.design_count
        
        return data
