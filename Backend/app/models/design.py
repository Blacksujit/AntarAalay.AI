"""
Module 3: Domain Models - Design

Design model representing AI-generated interior designs.

Dependencies: Module 2 (Database - Base), Module 3 (User, Room)
"""
from typing import TYPE_CHECKING, List, Dict, Any, Optional
from sqlalchemy import Column, String, DateTime, Float, ForeignKey, JSON
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from app.database import Base

# Type checking only imports
if TYPE_CHECKING:
    from app.models.user import User
    from app.models.room import Room


class Design(Base):
    """
    Design model representing an AI-generated interior design.
    """
    __tablename__ = "designs"
    __allow_unmapped__ = True  # SQLAlchemy 2.0 compatibility
    
    # Primary Key
    id = Column(String(36), primary_key=True, index=True, comment="UUID design identifier")
    
    # Foreign Keys
    room_id = Column(
        String(36),
        ForeignKey("rooms.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
        comment="Parent room ID"
    )
    user_id = Column(
        String(128),
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
        comment="Owner user ID (Firebase UID)"
    )
    
    # Design Parameters
    style = Column(String(50), nullable=False, comment="Design style: modern, traditional, minimalist, etc.")
    budget = Column(Float, nullable=True, comment="User's budget constraint")
    wall_color = Column(String(50), nullable=True, comment="Wall color preference")
    flooring_material = Column(String(50), nullable=True, comment="Flooring material preference")
    
    # Generated Images (3 variations)
    image_1_url = Column(String(512), nullable=True, comment="First design variation URL")
    image_2_url = Column(String(512), nullable=True, comment="Second design variation URL")
    image_3_url = Column(String(512), nullable=True, comment="Third design variation URL")
    
    # Budget Analysis
    estimated_cost = Column(Float, nullable=True, comment="Calculated estimated cost")
    budget_match_percentage = Column(Float, nullable=True, comment="Budget match percentage 0-100")
    furniture_breakdown = Column(JSON, nullable=True, comment="Itemized furniture costs as JSON")
    
    # Vastu Analysis
    vastu_score = Column(Float, nullable=True, comment="Vastu compliance score 0-100")
    vastu_suggestions = Column(JSON, nullable=True, comment="List of Vastu improvement suggestions")
    vastu_warnings = Column(JSON, nullable=True, comment="List of Vastu concerns")
    
    # Status
    status = Column(
        String(20),
        nullable=False,
        default="pending",
        comment="Status: pending, completed, failed"
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
    room: "Room" = relationship("Room", back_populates="designs")
    user: "User" = relationship("User", back_populates="designs")
    
    # Valid statuses
    VALID_STATUSES = ["pending", "completed", "failed"]
    
    # Vastu score thresholds
    VASTU_EXCELLENT = 80
    VASTU_GOOD = 60
    VASTU_NEUTRAL = 40
    
    def __repr__(self) -> str:
        """String representation of Design."""
        return f"<Design(id={self.id}, style={self.style}, status={self.status})>"
    
    def __str__(self) -> str:
        """Human-readable string representation."""
        return f"{self.style} design ({self.status})"
    
    @property
    def generated_images(self) -> List[str]:
        """Return list of all generated image URLs."""
        images = []
        if self.image_1_url:
            images.append(self.image_1_url)
        if self.image_2_url:
            images.append(self.image_2_url)
        if self.image_3_url:
            images.append(self.image_3_url)
        return images
    
    @property
    def has_images(self) -> bool:
        """Check if design has generated images."""
        return len(self.generated_images) > 0
    
    @property
    def has_budget_analysis(self) -> bool:
        """Check if budget analysis is complete."""
        return self.estimated_cost is not None and self.furniture_breakdown is not None
    
    @property
    def has_vastu_analysis(self) -> bool:
        """Check if Vastu analysis is complete."""
        return self.vastu_score is not None
    
    @property
    def is_completed(self) -> bool:
        """Check if design generation is completed."""
        return self.status == "completed"
    
    @property
    def is_pending(self) -> bool:
        """Check if design generation is pending."""
        return self.status == "pending"
    
    @property
    def is_failed(self) -> bool:
        """Check if design generation failed."""
        return self.status == "failed"
    
    @property
    def vastu_rating(self) -> str:
        """
        Return Vastu rating based on score.
        
        Returns:
            str: "excellent", "good", "neutral", or "poor"
        """
        if self.vastu_score is None:
            return "unknown"
        if self.vastu_score >= self.VASTU_EXCELLENT:
            return "excellent"
        if self.vastu_score >= self.VASTU_GOOD:
            return "good"
        if self.vastu_score >= self.VASTU_NEUTRAL:
            return "neutral"
        return "poor"
    
    @property
    def budget_status(self) -> str:
        """
        Return budget status based on match percentage.
        
        Returns:
            str: "under", "match", or "over"
        """
        if self.budget_match_percentage is None or self.budget is None:
            return "unknown"
        if self.budget_match_percentage <= 90:
            return "under"
        if self.budget_match_percentage <= 100:
            return "match"
        return "over"
    
    def is_valid_status(self) -> bool:
        """Check if status is valid."""
        return self.status in self.VALID_STATUSES
    
    def mark_completed(self) -> None:
        """Mark design as completed."""
        self.status = "completed"
    
    def mark_failed(self) -> None:
        """Mark design as failed."""
        self.status = "failed"
    
    def mark_pending(self) -> None:
        """Mark design as pending."""
        self.status = "pending"
    
    def set_images(self, images: List[str]) -> None:
        """
        Set generated image URLs.
        
        Args:
            images: List of image URLs (1-3 items)
        """
        self.image_1_url = images[0] if len(images) > 0 else None
        self.image_2_url = images[1] if len(images) > 1 else None
        self.image_3_url = images[2] if len(images) > 2 else None
    
    def to_dict(self, include_relations: bool = False) -> Dict[str, Any]:
        """
        Convert design to dictionary.
        
        Args:
            include_relations: Whether to include room/user IDs
            
        Returns:
            dict: Design data as dictionary
        """
        data = {
            "id": self.id,
            "style": self.style,
            "budget": self.budget,
            "status": self.status,
            "images": self.generated_images,
            "has_images": self.has_images,
            "estimated_cost": self.estimated_cost,
            "budget_match_percentage": self.budget_match_percentage,
            "budget_status": self.budget_status,
            "furniture_breakdown": self.furniture_breakdown,
            "vastu_score": self.vastu_score,
            "vastu_rating": self.vastu_rating,
            "vastu_suggestions": self.vastu_suggestions,
            "vastu_warnings": self.vastu_warnings,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }
        
        if include_relations:
            data["room_id"] = self.room_id
            data["user_id"] = self.user_id
        
        return data
