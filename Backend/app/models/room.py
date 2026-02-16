"""
Module 3: Domain Models - Room

Room model representing a physical room uploaded by a user.

Dependencies: Module 2 (Database - Base), Module 3 (User)
"""
from typing import TYPE_CHECKING, List, Optional
from sqlalchemy import Column, String, DateTime, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from app.database import Base

# Type checking only imports
if TYPE_CHECKING:
    from app.models.user import User
    from app.models.design import Design


class Room(Base):
    """
    Room model representing a physical room uploaded by a user.
    """
    __tablename__ = "rooms"
    __allow_unmapped__ = True  # SQLAlchemy 2.0 compatibility
    
    # Primary Key
    id = Column(String(36), primary_key=True, index=True, comment="UUID room identifier")
    
    # Foreign Key
    user_id = Column(
        String(128),
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
        comment="Owner user ID (Firebase UID)"
    )
    
    # Room Information
    image_url = Column(String(512), nullable=False, comment="S3 URL of room image")
    room_type = Column(
        String(50),
        nullable=True,
        comment="Room type: bedroom, living, kitchen, dining, study, bathroom"
    )
    direction = Column(
        String(20),
        nullable=True,
        comment="Vastu direction: north, south, east, west, northeast, northwest, southeast, southwest"
    )
    
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
    user: "User" = relationship("User", back_populates="rooms")
    
    designs: List["Design"] = relationship(
        "Design",
        back_populates="room",
        cascade="all, delete-orphan",
        lazy="dynamic"
    )
    
    # Valid room types
    VALID_ROOM_TYPES = [
        "bedroom",
        "living",
        "kitchen",
        "dining",
        "study",
        "bathroom"
    ]
    
    # Valid Vastu directions
    VALID_DIRECTIONS = [
        "north",
        "south",
        "east",
        "west",
        "northeast",
        "northwest",
        "southeast",
        "southwest"
    ]
    
    def __repr__(self) -> str:
        """String representation of Room."""
        return f"<Room(id={self.id}, type={self.room_type}, direction={self.direction})>"
    
    def __str__(self) -> str:
        """Human-readable string representation."""
        return f"{self.room_type or 'Room'} ({self.direction or 'unknown direction'})"
    
    @property
    def design_count(self) -> int:
        """Return number of designs generated for this room."""
        return list(self.designs).__len__() if self.designs else 0
    
    @property
    def has_vastu_data(self) -> bool:
        """Check if room has direction data for Vastu analysis."""
        return self.direction is not None and self.direction.lower() in self.VALID_DIRECTIONS
    
    def is_valid_room_type(self) -> bool:
        """Check if room_type is a valid type."""
        if not self.room_type:
            return True  # Optional field
        return self.room_type.lower() in self.VALID_ROOM_TYPES
    
    def is_valid_direction(self) -> bool:
        """Check if direction is a valid Vastu direction."""
        if not self.direction:
            return True  # Optional field
        return self.direction.lower() in self.VALID_DIRECTIONS
    
    def to_dict(self, include_relations: bool = False) -> dict:
        """
        Convert room to dictionary.
        
        Args:
            include_relations: Whether to include user and design IDs
            
        Returns:
            dict: Room data as dictionary
        """
        data = {
            "id": self.id,
            "image_url": self.image_url,
            "room_type": self.room_type,
            "direction": self.direction,
            "has_vastu_data": self.has_vastu_data,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }
        
        if include_relations:
            data["user_id"] = self.user_id
            data["design_ids"] = [d.id for d in self.designs] if self.designs else []
            data["design_count"] = self.design_count
        
        return data
