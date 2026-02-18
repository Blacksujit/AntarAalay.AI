"""
Test Suite for AI Interior Styling Engine

This module provides comprehensive tests for the AI engine components,
including unit tests, integration tests, and mock tests.

Test Coverage:
- Prompt builder correctness
- ControlNet edge detection
- Rate limiting logic
- Engine switching
- API integrations (mocked)
- End-to-end workflows
"""

import sys
import os
from pathlib import Path

# Add backend directory to Python path
backend_dir = Path(__file__).parent.parent.parent
sys.path.insert(0, str(backend_dir))

import pytest
import asyncio
import io
import base64
from unittest.mock import Mock, patch, AsyncMock
from PIL import Image
import numpy as np

# Import AI engine components
from app.services.ai_engine import (
    EngineFactory,
    GenerationRequest,
    GenerationResult,
    EngineType,
    PromptBuilder,
    StyleParameters,
    ControlNetAdapter,
    RateLimiter,
    RateLimitConfig,
    RateLimitError
)


class TestPromptBuilder:
    """Test cases for PromptBuilder."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.prompt_builder = PromptBuilder()
    
    def test_build_positive_prompt_basic(self):
        """Test basic positive prompt building."""
        style_params = StyleParameters(
            room_type='living',
            furniture_style='modern',
            wall_color='white',
            flooring_material='hardwood'
        )
        
        prompt = self.prompt_builder.build_positive_prompt(style_params)
        
        assert 'living room' in prompt
        assert 'modern minimalist furniture' in prompt
        assert 'crisp white' in prompt
        assert 'natural hardwood flooring' in prompt
        assert 'Preserve original room geometry' in prompt
    
    def test_build_negative_prompt(self):
        """Test negative prompt building."""
        negative = self.prompt_builder.build_negative_prompt()
        
        assert 'distorted perspective' in negative
        assert 'floating furniture' in negative
        assert 'warped walls' in negative
        assert 'low resolution' in negative
    
    def test_style_parameter_validation(self):
        """Test style parameter validation."""
        # Valid parameters
        valid_params = StyleParameters(
            room_type='bedroom',
            furniture_style='scandinavian',
            wall_color='blue',
            flooring_material='tile'
        )
        
        is_valid, error = self.prompt_builder.validate_style_parameters(valid_params)
        assert is_valid is True
        assert error is None
        
        # Invalid parameters (missing room_type)
        invalid_params = StyleParameters(
            room_type='',
            furniture_style='modern',
            wall_color='white',
            flooring_material='hardwood'
        )
        
        is_valid, error = self.prompt_builder.validate_style_parameters(invalid_params)
        assert is_valid is False
        assert 'Room type is required' in error
    
    def test_prompt_hash_generation(self):
        """Test prompt hash generation."""
        style_params = StyleParameters(
            room_type='living',
            furniture_style='modern',
            wall_color='white',
            flooring_material='hardwood'
        )
        
        hash1 = self.prompt_builder.get_prompt_hash(style_params)
        hash2 = self.prompt_builder.get_prompt_hash(style_params)
        
        assert hash1 == hash2
        assert len(hash1) == 8  # MD5 hash truncated to 8 chars
    
    def test_controlnet_prompt_optimization(self):
        """Test ControlNet-optimized prompts."""
        style_params = StyleParameters(
            room_type='kitchen',
            furniture_style='industrial',
            wall_color='gray',
            flooring_material='concrete'
        )
        
        prompts = self.prompt_builder.build_controlnet_prompt(style_params, weight=1.2)
        
        assert 'positive' in prompts
        assert 'negative' in prompts
        assert 'kitchen' in prompts['positive']
        assert 'industrial' in prompts['positive']


class TestControlNetAdapter:
    """Test cases for ControlNetAdapter."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.config = {
            'default_resolution': (512, 512),
            'edge_method': 'canny',
            'canny_low_threshold': 50,
            'canny_high_threshold': 150
        }
        self.adapter = ControlNetAdapter(self.config)
    
    def create_test_image(self, width=512, height=512, color='white'):
        """Create a test image."""
        image = Image.new('RGB', (width, height), color=color)
        buffer = io.BytesIO()
        image.save(buffer, format='PNG')
        return buffer.getvalue()
    
    def test_image_preprocessing(self):
        """Test image preprocessing."""
        image_bytes = self.create_test_image()
        
        processed = self.adapter.preprocess_image(image_bytes)
        
        assert isinstance(processed, np.ndarray)
        assert processed.shape[2] == 3  # RGB channels
    
    def test_resolution_normalization(self):
        """Test resolution normalization."""
        # Create larger image
        image_bytes = self.create_test_image(1024, 768)
        processed = self.adapter.preprocess_image(image_bytes)
        
        normalized = self.adapter.normalize_resolution(processed, (512, 512))
        
        assert normalized.shape[:2] == (512, 512)
    
    def test_canny_edge_detection(self):
        """Test Canny edge detection."""
        # Create test image with some contrast
        image_bytes = self.create_test_image()
        processed = self.adapter.preprocess_image(image_bytes)
        
        edges = self.adapter.detect_canny_edges(processed)
        
        assert isinstance(edges, np.ndarray)
        assert len(edges.shape) == 2  # Grayscale
        assert edges.dtype == np.uint8
    
    def test_controlnet_preprocessing(self):
        """Test ControlNet preprocessing pipeline."""
        image_bytes = self.create_test_image()
        
        edge_bytes = self.adapter.preprocess_for_controlnet(
            image_bytes,
            target_resolution=(512, 512),
            edge_method='canny'
        )
        
        assert isinstance(edge_bytes, bytes)
        
        # Verify it's a valid PNG
        edge_image = Image.open(io.BytesIO(edge_bytes))
        assert edge_image.mode == 'L'  # Grayscale
    
    def test_edge_map_validation(self):
        """Test edge map validation."""
        image_bytes = self.create_test_image()
        edge_bytes = self.adapter.preprocess_for_controlnet(image_bytes)
        
        is_valid, error = self.adapter.validate_edge_map(edge_bytes)
        
        assert is_valid is True
        assert error is None
    
    def test_edge_statistics(self):
        """Test edge statistics calculation."""
        image_bytes = self.create_test_image()
        edge_bytes = self.adapter.preprocess_for_controlnet(image_bytes)
        
        stats = self.adapter.get_edge_statistics(edge_bytes)
        
        assert 'resolution' in stats
        assert 'edge_ratio' in stats
        assert 'mean_intensity' in stats


class TestRateLimiter:
    """Test cases for RateLimiter."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.config = RateLimitConfig(
            free_daily_limit=3,
            authenticated_daily_limit=5,
            global_requests_per_minute=10
        )
        self.rate_limiter = RateLimiter(self.config)
    
    @pytest.mark.asyncio
    async def test_rate_limit_check_free_user(self):
        """Test rate limiting for free users."""
        user_data = {'uid': 'test_user'}  # Free user
        
        # First request should be allowed
        allowed, error = await self.rate_limiter.check_rate_limit('user1', user_data)
        assert allowed is True
        assert error is None
        
        # Use up daily limit
        for i in range(self.config.free_daily_limit - 1):
            allowed, _ = await self.rate_limiter.check_rate_limit('user1', user_data)
            assert allowed is True
        
        # Next request should be blocked
        allowed, error = await self.rate_limiter.check_rate_limit('user1', user_data)
        assert allowed is False
        assert 'Daily generation limit' in error
    
    @pytest.mark.asyncio
    async def test_rate_limit_check_authenticated_user(self):
        """Test rate limiting for authenticated users."""
        user_data = {'uid': 'test_user', 'email_verified': True}
        
        # Use up authenticated user limit
        for i in range(self.config.authenticated_daily_limit):
            allowed, _ = await self.rate_limiter.check_rate_limit('user2', user_data)
            assert allowed is True
        
        # Next request should be blocked
        allowed, error = await self.rate_limiter.check_rate_limit('user2', user_data)
        assert allowed is False
        assert 'Daily generation limit' in error
    
    @pytest.mark.asyncio
    async def test_global_rate_limiting(self):
        """Test global rate limiting."""
        user_data = {'uid': 'test_user'}
        
        # Fill up global limit
        for i in range(self.config.global_requests_per_minute):
            allowed, _ = await self.rate_limiter.check_rate_limit(f'user{i}', user_data)
            assert allowed is True
        
        # Next request should be blocked by global limit
        allowed, error = await self.rate_limiter.check_rate_limit('user_final', user_data)
        assert allowed is False
        assert 'high demand' in error
    
    @pytest.mark.asyncio
    async def test_user_usage_tracking(self):
        """Test user usage tracking."""
        user_data = {'uid': 'test_user'}
        
        # Make some requests
        await self.rate_limiter.check_rate_limit('user1', user_data)
        await self.rate_limiter.check_rate_limit('user1', user_data)
        
        usage = await self.rate_limiter.get_user_usage('user1')
        
        assert usage['count'] == 2
        assert usage['limit'] == self.config.free_daily_limit
        assert usage['remaining'] == self.config.free_daily_limit - 2


class TestEngineFactory:
    """Test cases for EngineFactory."""
    
    def test_engine_type_creation(self):
        """Test creating engines by type."""
        config = {'device': 'cpu'}
        
        # Test local SDXL engine creation
        engine = EngineFactory.create_engine(EngineType.LOCAL_SDXL, config)
        assert engine.engine_type == EngineType.LOCAL_SDXL
        
        # Test Replicate engine creation
        with patch('app.services.ai_engine.replicate_img2img_engine.ReplicateEngine'):
            engine = EngineFactory.create_engine(EngineType.REPLICATE, config)
            assert engine.engine_type == EngineType.REPLICATE
    
    @patch('app.services.ai_engine.base_engine.get_settings')
    def test_engine_from_environment(self, mock_settings):
        """Test engine creation from environment."""
        mock_settings.return_value = Mock(
            AI_ENGINE='local_sdxl',
            DEVICE='cpu',
            SDXL_MODEL_PATH='test/model',
            CONTROLNET_MODEL='test/controlnet',
            REPLICATE_API_TOKEN=None,
            HF_API_KEY=None
        )
        
        engine = EngineFactory.get_engine_from_env()
        assert engine.engine_type == EngineType.LOCAL_SDXL


class TestGenerationRequest:
    """Test cases for GenerationRequest."""
    
    def test_request_validation(self):
        """Test generation request validation."""
        engine = EngineFactory.create_engine(EngineType.LOCAL_SDXL, {'device': 'cpu'})
        
        # Valid request
        valid_request = GenerationRequest(
            primary_image=b'fake_image_data',
            room_images={'north': b'fake_image_data'},
            room_type='living',
            furniture_style='modern',
            wall_color='white',
            flooring_material='hardwood'
        )
        
        is_valid, error = engine.validate_request(valid_request)
        assert is_valid is True
        assert error is None
        
        # Invalid request (no primary image)
        invalid_request = GenerationRequest(
            primary_image=b'',
            room_images={'north': b'fake_image_data'},
            room_type='living',
            furniture_style='modern',
            wall_color='white',
            flooring_material='hardwood'
        )
        
        is_valid, error = engine.validate_request(invalid_request)
        assert is_valid is False
        assert 'Primary image is required' in error


class TestIntegration:
    """Integration tests for the complete AI engine system."""
    
    @pytest.mark.asyncio
    async def test_end_to_end_workflow(self):
        """Test complete workflow from request to result."""
        # Mock the entire pipeline
        with patch('app.services.ai_engine.local_sdxl_img2img_engine.LocalSDXLEngine') as mock_engine:
            # Setup mock engine
            mock_instance = Mock()
            mock_instance.generate_img2img.return_value = GenerationResult(
                success=True,
                generated_images=['http://example.com/image1.jpg'],
                engine_used='local_sdxl',
                seeds_used=[42, 123, 456]
            )
            mock_engine.return_value = mock_instance
            
            # Create test request
            request = GenerationRequest(
                primary_image=b'fake_image_data',
                room_images={'north': b'fake_image_data'},
                room_type='living',
                furniture_style='modern',
                wall_color='white',
                flooring_material='hardwood'
            )
            
            # Execute workflow
            result = await mock_instance.generate_img2img(request)
            
            # Verify result
            assert result.success is True
            assert len(result.generated_images) == 1
            assert result.engine_used == 'local_sdxl'
    
    @pytest.mark.asyncio
    async def test_rate_limit_integration(self):
        """Test rate limiting integration with generation."""
        with patch('app.services.ai_design_service.check_generation_rate_limit') as mock_rate_limit:
            # Setup rate limit to allow request
            mock_rate_limit.return_value = (True, None)
            
            from app.services.ai_design_service import AIDesignService
            service = AIDesignService()
            
            # Mock the AI engine
            with patch.object(service, '_get_engine') as mock_get_engine:
                mock_engine = Mock()
                mock_engine.health_check.return_value = True
                mock_engine.generate_img2img.return_value = GenerationResult(
                    success=True,
                    generated_images=['http://example.com/image1.jpg']
                )
                mock_get_engine.return_value = mock_engine
                
                # Mock room validation
                with patch.object(service, '_validate_room_images') as mock_validate:
                    mock_validate.return_value = {'north': b'fake_image'}
                    
                    # Execute generation
                    result = await service.generate_design(
                        user_id='test_user',
                        user_data={'uid': 'test_user'},
                        room_id='test_room',
                        room_type='living',
                        furniture_style='modern',
                        wall_color='white',
                        flooring_material='hardwood'
                    )
                    
                    # Verify rate limit was checked
                    mock_rate_limit.assert_called_once()
                    assert result['status'] == 'completed'


# Mock fixtures for external API testing
@pytest.fixture
def mock_replicate_response():
    """Mock Replicate API response."""
    return {
        'id': 'test_prediction_id',
        'status': 'succeeded',
        'output': ['http://example.com/generated_image.jpg']
    }


@pytest.fixture
def mock_hf_response():
    """Mock HuggingFace API response."""
    # Base64 encoded 1x1 pixel image
    tiny_image = base64.b64encode(
        b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00\x01'
        b'\x08\x02\x00\x00\x00\x90wS\xde\x00\x00\x00\tpHYs\x00\x00\x0b\x13'
        b'\x00\x00\x0b\x13\x01\x00\x9a\x9c\x18\x00\x00\x00\nIDATx\x9cc\xf8'
        b'\x00\x00\x00\x01\x00\x01\x00\x00\x00\x00IEND\xaeB`\x82'
    ).decode('utf-8')
    
    return [tiny_image]


if __name__ == '__main__':
    # Run tests
    pytest.main([__file__, '-v'])
