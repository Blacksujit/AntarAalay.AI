"""
Tests for Module 5 (AI Engine) and Module 6 (Vastu Engine)
"""
import sys
import os
from pathlib import Path

# Add backend directory to Python path
backend_dir = Path(__file__).parent.parent.parent
sys.path.insert(0, str(backend_dir))

import pytest
from unittest.mock import Mock, patch

from app.services.ai_engine import AIEngine, AIEngineError, get_ai_engine
from app.services.vastu_engine import VastuEngine, VastuEngineError, InvalidDirectionError, get_vastu_engine


class TestAIEngine:
    """Test cases for AI Engine."""
    
    def test_style_prompts_constant(self):
        """Test that style prompts are defined."""
        assert "modern" in AIEngine.STYLE_PROMPTS
        assert "traditional" in AIEngine.STYLE_PROMPTS
        assert "minimalist" in AIEngine.STYLE_PROMPTS
        
    def test_build_prompt(self):
        """Test prompt building for different styles."""
        engine = AIEngine()
        
        modern_prompt = engine._build_prompt("modern", "bedroom")
        assert "modern" in modern_prompt.lower()
        assert "bedroom" in modern_prompt.lower()
        
    def test_generate_mock_urls(self):
        """Test mock URL generation."""
        engine = AIEngine()
        urls = engine._generate_mock_urls("modern")
        
        assert len(urls) == 3
        assert all("Modern" in url for url in urls)
        
    @patch('app.services.ai_engine.requests.post')
    def test_call_stable_diffusion_success(self, mock_post):
        """Test successful API call."""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"image": "base64data"}
        mock_post.return_value = mock_response
        
        engine = AIEngine()
        engine.api_key = "test-key"
        
        result = engine._call_stable_diffusion("test prompt", 0)
        
        assert result is not None
        mock_post.assert_called_once()
        
    @patch('app.services.ai_engine.requests.post')
    def test_call_stable_diffusion_failure(self, mock_post):
        """Test failed API call."""
        mock_response = Mock()
        mock_response.status_code = 500
        mock_response.text = "Error"
        mock_post.return_value = mock_response
        
        engine = AIEngine()
        engine.api_key = "test-key"
        
        result = engine._call_stable_diffusion("test prompt", 0)
        
        assert result is None
        
    def test_generate_without_api_key_returns_mock(self):
        """Test that mock URLs are returned when no API key."""
        engine = AIEngine()
        engine.api_key = ""
        
        urls = engine.generate_design_variations("http://image.jpg", "modern", "bedroom")
        
        assert len(urls) == 3
        assert all("placehold.co" in url for url in urls)


class TestVastuEngine:
    """Test cases for Vastu Engine."""
    
    def test_analyze_excellent_score(self):
        """Test Vastu analysis for excellent score."""
        engine = VastuEngine()
        
        # Bedroom in southwest should have excellent score
        result = engine.analyze("southwest", "bedroom")
        
        assert result["vastu_score"] == 100
        assert result["direction_rating"] == "excellent"
        assert "element_balance" in result
        assert result["element_balance"]["dominant_element"] == "Earth"
        
    def test_analyze_poor_score(self):
        """Test Vastu analysis for poor score."""
        engine = VastuEngine()
        
        # Bedroom in northeast should have poor score
        result = engine.analyze("northeast", "bedroom")
        
        assert result["vastu_score"] == 20
        assert result["direction_rating"] == "poor"
        assert len(result["warnings"]) > 0
        
    def test_analyze_invalid_direction(self):
        """Test Vastu analysis with invalid direction."""
        engine = VastuEngine()
        
        # Invalid direction should return unknown direction with minimal score
        result = engine.analyze("invalid", "bedroom")
        assert result["direction"] == "unknown"
        assert result["vastu_score"] == 50  # Neutral default
            
    def test_get_remedies_northeast_kitchen(self):
        """Test remedies for northeast kitchen."""
        engine = VastuEngine()
        
        remedies = engine.get_remedies("northeast", "kitchen")
        
        assert len(remedies) > 0
        assert any("pyramid" in r.lower() for r in remedies)
        
    def test_get_remedies_general(self):
        """Test general remedies."""
        engine = VastuEngine()
        
        remedies = engine.get_remedies("north", "bedroom")
        
        assert len(remedies) > 0
        assert any("clean" in r.lower() for r in remedies)
        
    def test_all_directions_have_rules(self):
        """Test that all 8 directions have rules defined."""
        directions = ["north", "south", "east", "west", "northeast", "northwest", "southeast", "southwest"]
        engine = VastuEngine()
        
        for direction in directions:
            assert direction in engine.rules
            
            
    def test_all_room_types_have_scores(self):
        """Test that all room types have score mappings."""
        room_types = ["bedroom", "living", "kitchen", "dining", "study", "bathroom"]
        engine = VastuEngine()
        
        for room_type in room_types:
            assert room_type in engine.room_scores


class TestEngineSingletons:
    """Test singleton patterns for engines."""
    
    def test_get_ai_engine_singleton(self):
        """Test AI engine singleton."""
        engine1 = get_ai_engine()
        engine2 = get_ai_engine()
        
        assert engine1 is engine2
        
    def test_get_vastu_engine_singleton(self):
        """Test Vastu engine singleton."""
        engine1 = get_vastu_engine()
        engine2 = get_vastu_engine()
        
        assert engine1 is engine2


# Run with: pytest tests/test_engines.py -v
