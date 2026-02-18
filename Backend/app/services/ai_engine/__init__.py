"""
AI Engine Module for Interior Styling

This module provides a complete AI image-to-image transformation system
for interior design with layout preservation.

Components:
- BaseEngine: Abstract interface for all AI engines
- LocalSDXLEngine: Local SDXL with ControlNet for development
- ReplicateEngine: Replicate API integration for production
- HFEngine: HuggingFace Inference API integration
- PromptBuilder: Optimized prompt generation for interiors
- ControlNetAdapter: Edge detection and layout preservation
- RateLimiter: Usage quotas and cost control

Usage:
    from app.services.ai_engine import EngineFactory, GenerationRequest
    
    # Create engine based on environment
    engine = EngineFactory.get_engine_from_env()
    
    # Prepare generation request
    request = GenerationRequest(
        primary_image=image_bytes,
        room_images={'north': north_image, 'south': south_image, ...},
        room_type='living',
        furniture_style='modern',
        wall_color='white',
        flooring_material='hardwood'
    )
    
    # Generate images
    result = await engine.generate_img2img(request)
"""

from .base_engine import (
    BaseEngine,
    GenerationRequest,
    GenerationResult,
    EngineType,
    EngineFactory
)

from .local_sdxl_img2img_engine import LocalSDXLEngine
from .replicate_img2img_engine import ReplicateEngine
from .hf_img2img_engine import HFEngine

from .prompt_builder import PromptBuilder, StyleParameters
from .controlnet_adapter import ControlNetAdapter
from .rate_limiter import (
    RateLimiter,
    RateLimitConfig,
    get_rate_limiter,
    check_generation_rate_limit,
    RateLimitError
)

__all__ = [
    # Core interfaces
    'BaseEngine',
    'GenerationRequest',
    'GenerationResult',
    'EngineType',
    'EngineFactory',
    
    # Engine implementations
    'LocalSDXLEngine',
    'ReplicateEngine',
    'HFEngine',
    
    # Supporting modules
    'PromptBuilder',
    'StyleParameters',
    'ControlNetAdapter',
    'RateLimiter',
    'RateLimitConfig',
    
    # Utility functions
    'get_rate_limiter',
    'check_generation_rate_limit',
    'RateLimitError'
]

# Version info
__version__ = '1.0.0'
__author__ = 'AntarAalay.ai ML Team'
__description__ = 'AI Interior Styling Engine with Layout Preservation'
