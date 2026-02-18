#!/usr/bin/env python3
"""
Demo Design Service - Returns sample designs when API quota exceeded
"""

import uuid
import json
from datetime import datetime
from typing import List, Dict, Any

class DemoDesignService:
    """
    Provides demo/sample designs when AI API is unavailable.
    Uses cached professional interior design images.
    """
    
    # Sample high-quality interior design images (placeholder URLs - replace with actual samples)
    SAMPLE_DESIGNS = [
        {
            "id": "demo-modern-1",
            "style": "modern",
            "image_url": "https://images.unsplash.com/photo-1600210492486-724fe5c67fb0?w=800",
            "estimated_cost": 45000,
            "budget_match": 90,
            "vastu_score": 85,
        },
        {
            "id": "demo-modern-2", 
            "style": "modern",
            "image_url": "https://images.unsplash.com/photo-1600607687939-ce8a6c25118c?w=800",
            "estimated_cost": 52000,
            "budget_match": 85,
            "vastu_score": 88,
        },
        {
            "id": "demo-minimalist-1",
            "style": "minimalist", 
            "image_url": "https://images.unsplash.com/photo-1600585154340-be6161a56a0c?w=800",
            "estimated_cost": 38000,
            "budget_match": 95,
            "vastu_score": 82,
        }
    ]
    
    @staticmethod
    def generate_demo_designs(room_id: str, style: str, wall_color: str, flooring: str, user_id: str = "dev-user") -> Dict[str, Any]:
        """
        Generate demo designs when AI API is unavailable.
        
        Returns:
            Dict with design data matching the normal API response format
        """
        design_id = str(uuid.uuid4())
        
        # Select designs based on requested style
        matching_designs = [d for d in DemoDesignService.SAMPLE_DESIGNS if d["style"] == style.lower()]
        if not matching_designs:
            matching_designs = DemoDesignService.SAMPLE_DESIGNS  # Fallback to any style
        
        # Create 3 variations
        designs = []
        for i, template in enumerate(matching_designs[:3]):
            design = {
                "id": f"{design_id}_{i+1}",
                "room_id": room_id,  # Use the actual room_id provided
                "user_id": user_id,  # Use the actual user_id provided
                "style": style,
                "wall_color": wall_color,
                "flooring_material": flooring,
                "image_1_url": template["image_url"],
                "image_2_url": matching_designs[(i+1) % len(matching_designs)]["image_url"],
                "image_3_url": matching_designs[(i+2) % len(matching_designs)]["image_url"],
                "estimated_cost": template["estimated_cost"],
                "budget_match_percentage": template["budget_match"],
                "furniture_breakdown": json.dumps({  # Convert to JSON string for database
                    "sofa": {"adjusted_price": 15000, "base_price": 12000, "quantity": 1},
                    "table": {"adjusted_price": 8000, "base_price": 6000, "quantity": 1},
                    "chairs": {"adjusted_price": 5000, "base_price": 4000, "quantity": 2}
                }),
                "vastu_score": template["vastu_score"],
                "vastu_suggestions": ["Good natural lighting", "Proper furniture placement", "Balanced room layout"],  # Keep as array
                "vastu_warnings": [],  # Keep as array
                "status": "completed",
                "created_at": datetime.utcnow(),  # Use datetime object, not string
                "is_demo": True  # Flag to indicate this is a demo design
            }
            designs.append(design)
        
        return {
            "design_id": design_id,
            "designs": designs,
            "status": "success",
            "message": "Demo designs generated (AI generation temporarily unavailable)",
            "is_demo_mode": True
        }
    
    @staticmethod
    def is_demo_design(design: Dict) -> bool:
        """Check if a design is a demo design."""
        return design.get("is_demo", False)

# Global instance
demo_service = DemoDesignService()
