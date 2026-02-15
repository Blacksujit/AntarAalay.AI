"""
Module 7: Budget Engine

This module handles budget calculations and furniture cost estimation.

Dependencies: Module 1 (Configuration)
"""
from typing import Dict, List, Optional
import logging

logger = logging.getLogger(__name__)


class BudgetEngineError(Exception):
    """Raised when budget calculation fails."""
    pass


class BudgetEngine:
    """
    Budget Engine for calculating furniture costs and budget compatibility.
    
    Provides price estimates based on room type, style, and user budget.
    """
    
    # Furniture prices in INR
    FURNITURE_PRICES = {
        "sofa": 25000,
        "bed": 18000,
        "table": 12000,
        "decor": 8000,
        "chair": 5000,
        "wardrobe": 15000,
        "tv_unit": 10000,
        "bookshelf": 7000,
        "rug": 4000,
        "lighting": 6000,
        "curtains": 5000,
        "pillows": 2000,
        "wall_art": 3000,
        "plant": 1500,
        "mirror": 3500
    }
    
    # Style multipliers
    STYLE_MULTIPLIERS = {
        "modern": 1.2,
        "traditional": 1.0,
        "minimalist": 0.9,
        "luxury": 2.0,
        "bohemian": 0.85,
        "industrial": 1.1,
        "scandinavian": 1.0,
        "contemporary": 1.3
    }
    
    # Room type furniture requirements
    ROOM_FURNITURE = {
        "bedroom": ["bed", "wardrobe", "curtains", "lighting", "rug", "wall_art", "mirror"],
        "living": ["sofa", "tv_unit", "rug", "lighting", "curtains", "wall_art", "plant", "pillows"],
        "kitchen": ["table", "chair", "lighting", "wall_art"],
        "dining": ["table", "chair", "lighting", "wall_art", "rug"],
        "study": ["table", "chair", "bookshelf", "lighting", "wall_art"],
        "bathroom": ["mirror", "lighting", "decor"]
    }
    
    def calculate_estimate(
        self,
        room_type: str,
        style: str,
        budget: Optional[float] = None
    ) -> Dict:
        """
        Calculate budget estimate for a room design.
        
        Args:
            room_type: Type of room
            style: Design style
            budget: User's budget constraint (optional)
            
        Returns:
            Dict with estimated_cost, budget_match_percentage, furniture_breakdown
            
        Raises:
            BudgetEngineError: If calculation fails
        """
        try:
            # Get furniture list for room type
            furniture_list = self.ROOM_FURNITURE.get(room_type, self.ROOM_FURNITURE["living"])
            
            # Calculate base cost
            base_cost = sum(self.FURNITURE_PRICES.get(item, 5000) for item in furniture_list)
            
            # Apply style multiplier
            multiplier = self.STYLE_MULTIPLIERS.get(style.lower(), 1.0)
            estimated_cost = base_cost * multiplier
            
            # Build furniture breakdown
            breakdown = {}
            for item in furniture_list:
                base_price = self.FURNITURE_PRICES.get(item, 5000)
                adjusted_price = base_price * multiplier
                breakdown[item] = {
                    "base_price": base_price,
                    "adjusted_price": round(adjusted_price, 2),
                    "quantity": 1
                }
            
            # Calculate budget match percentage
            budget_match = None
            if budget and budget > 0:
                budget_match = min(100, round((estimated_cost / budget) * 100, 1))
            
            return {
                "estimated_cost": round(estimated_cost, 2),
                "budget": budget,
                "budget_match_percentage": budget_match,
                "furniture_breakdown": breakdown,
                "style_multiplier": multiplier,
                "furniture_count": len(furniture_list)
            }
            
        except Exception as e:
            logger.error(f"Budget calculation failed: {e}")
            raise BudgetEngineError(f"Failed to calculate budget: {str(e)}")
    
    def get_style_suggestions(self, budget: float, room_type: str) -> List[str]:
        """
        Get style suggestions based on budget.
        
        Args:
            budget: User's budget
            room_type: Type of room
            
        Returns:
            List of suggestion strings
        """
        suggestions = []
        
        furniture_list = self.ROOM_FURNITURE.get(room_type, self.ROOM_FURNITURE["living"])
        base_cost_min = sum(self.FURNITURE_PRICES.get(item, 5000) * 0.8 for item in furniture_list)
        base_cost_max = sum(self.FURNITURE_PRICES.get(item, 5000) * 1.5 for item in furniture_list)
        
        if budget < base_cost_min:
            suggestions.append("Consider minimalist or bohemian style for budget-friendly options")
            suggestions.append("Focus on key pieces and add decor gradually")
        elif budget > base_cost_max * 1.5:
            suggestions.append("Luxury style would fit your budget well")
            suggestions.append("Consider premium materials and custom furniture")
        else:
            suggestions.append("Modern or traditional styles would work well with your budget")
        
        return suggestions


# Global instance
_budget_engine: Optional[BudgetEngine] = None


def get_budget_engine() -> BudgetEngine:
    """Get or create global budget engine instance."""
    global _budget_engine
    if _budget_engine is None:
        _budget_engine = BudgetEngine()
    return _budget_engine


__all__ = ["BudgetEngine", "BudgetEngineError", "get_budget_engine"]
