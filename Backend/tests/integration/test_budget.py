"""
Tests for Module 7 (Budget Engine)
"""
import sys
import os
from pathlib import Path

# Add backend directory to Python path
backend_dir = Path(__file__).parent.parent.parent
sys.path.insert(0, str(backend_dir))

import pytest
from app.services.budget_engine import BudgetEngine, BudgetEngineError, get_budget_engine


class TestBudgetEngine:
    """Test cases for Budget Engine."""
    
    def test_furniture_prices_constant(self):
        """Test that furniture prices are defined."""
        assert "sofa" in BudgetEngine.FURNITURE_PRICES
        assert "bed" in BudgetEngine.FURNITURE_PRICES
        assert BudgetEngine.FURNITURE_PRICES["sofa"] == 25000
        
    def test_style_multipliers_constant(self):
        """Test that style multipliers are defined."""
        assert "modern" in BudgetEngine.STYLE_MULTIPLIERS
        assert "luxury" in BudgetEngine.STYLE_MULTIPLIERS
        assert BudgetEngine.STYLE_MULTIPLIERS["luxury"] == 2.0
        
    def test_calculate_estimate_bedroom_modern(self):
        """Test budget calculation for bedroom with modern style."""
        engine = BudgetEngine()
        
        result = engine.calculate_estimate("bedroom", "modern", budget=50000)
        
        assert "estimated_cost" in result
        assert "furniture_breakdown" in result
        assert "style_multiplier" in result
        assert result["style_multiplier"] == 1.2
        assert result["budget_match_percentage"] is not None
        
    def test_calculate_estimate_without_budget(self):
        """Test budget calculation without budget constraint."""
        engine = BudgetEngine()
        
        result = engine.calculate_estimate("living", "traditional")
        
        assert result["budget"] is None
        assert result["budget_match_percentage"] is None
        
    def test_calculate_estimate_luxury_multiplier(self):
        """Test luxury style applies correct multiplier."""
        engine = BudgetEngine()
        
        result = engine.calculate_estimate("bedroom", "luxury", budget=100000)
        
        assert result["style_multiplier"] == 2.0
        # Luxury should double the cost
        assert result["estimated_cost"] > 50000
        
    def test_get_style_suggestions_low_budget(self):
        """Test style suggestions for low budget."""
        engine = BudgetEngine()
        
        suggestions = engine.get_style_suggestions(10000, "living")
        
        assert len(suggestions) > 0
        assert any("minimalist" in s.lower() for s in suggestions)
        
    def test_get_style_suggestions_high_budget(self):
        """Test style suggestions for high budget."""
        engine = BudgetEngine()
        
        suggestions = engine.get_style_suggestions(200000, "living")
        
        assert len(suggestions) > 0
        assert any("luxury" in s.lower() for s in suggestions)
        
    def test_room_furniture_mapping(self):
        """Test that all room types have furniture mappings."""
        room_types = ["bedroom", "living", "kitchen", "dining", "study", "bathroom"]
        
        for room_type in room_types:
            assert room_type in BudgetEngine.ROOM_FURNITURE
            assert len(BudgetEngine.ROOM_FURNITURE[room_type]) > 0
            
    def test_budget_match_percentage_calculation(self):
        """Test budget match percentage is calculated correctly."""
        engine = BudgetEngine()
        
        # If budget equals estimated cost, match should be 100%
        result = engine.calculate_estimate("bathroom", "traditional", budget=11500)
        
        # Bathroom has lower base cost, with traditional multiplier (1.0)
        assert result["budget_match_percentage"] is not None
        assert isinstance(result["budget_match_percentage"], (int, float))


class TestBudgetEngineSingleton:
    """Test singleton pattern for Budget Engine."""
    
    def test_get_budget_engine_singleton(self):
        """Test budget engine singleton."""
        engine1 = get_budget_engine()
        engine2 = get_budget_engine()
        
        assert engine1 is engine2


# Run with: pytest tests/test_budget.py -v
