"""
Base AI Engine Architecture for Interior Styling

This module defines the abstract base class and common interfaces
for all AI image-to-image transformation engines.

Strategy Pattern Implementation:
- BaseEngine: Abstract interface
- LocalSDXLEngine: Development with local GPU
- ReplicateEngine: Production with Replicate API
- HFEngine: Production with HuggingFace Inference
"""

from abc import ABC, abstractmethod
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass
from enum import Enum
import logging

logger = logging.getLogger(__name__)


class EngineType(Enum):
    """Supported AI engine types."""
    LOCAL_SDXL = "local_sdxl"
    REPLICATE = "replicate"
    HF_INFERENCE = "hf_inference"
    HUGGINGFACE = "huggingface"
    STATE_OF_THE_ART = "state_of_the_art"
    POLLINATIONS = "pollinations"  # FREE AI generation
    SD15_CONTROLNET = "sd15_controlnet"  # Local GTX 1650 GPU


@dataclass
class GenerationRequest:
    """Image-to-image generation request parameters."""
    primary_image: bytes  # Main reference image (north direction)
    room_images: Dict[str, bytes]  # All 4 directional images
    room_type: str
    furniture_style: str
    wall_color: str
    flooring_material: str
    controlnet_weight: float = 1.0
    image_strength: float = 0.4
    num_inference_steps: int = 30
    guidance_scale: float = 7.0
    resolution: Tuple[int, int] = (512, 512)
    seeds: Optional[List[int]] = None


@dataclass
class GenerationResult:
    """Result of image-to-image generation."""
    success: bool
    generated_images: List[str]  # URLs to generated images
    error_message: Optional[str] = None
    engine_used: Optional[str] = None
    model_version: Optional[str] = None
    generation_params: Optional[Dict[str, Any]] = None
    seeds_used: Optional[List[int]] = None
    inference_time_seconds: Optional[float] = None


class BaseEngine(ABC):
    """
    Abstract base class for AI image-to-image transformation engines.
    
    All engines must implement this interface to ensure consistency
    across different providers (local, Replicate, HF).
    """
    
    def __init__(self, config: Dict[str, Any]):
        """
        Initialize the engine with configuration.
        
        Args:
            config: Engine-specific configuration dictionary
        """
        self.config = config
        self.engine_type = self._get_engine_type()
        self.logger = logging.getLogger(f"{__name__}.{self.engine_type}")
    
    @abstractmethod
    def _get_engine_type(self) -> EngineType:
        """Return the engine type identifier."""
        pass
    
    @abstractmethod
    async def generate_img2img(
        self, 
        request: GenerationRequest
    ) -> GenerationResult:
        """
        Generate image-to-image transformations.
        
        Args:
            request: Generation parameters and input images
            
        Returns:
            GenerationResult with URLs to generated images
        """
        pass
    
    @abstractmethod
    async def health_check(self) -> bool:
        """
        Check if the engine is available and healthy.
        
        Returns:
            True if engine is operational
        """
        pass
    
    @abstractmethod
    def get_model_info(self) -> Dict[str, Any]:
        """
        Get information about the loaded model.
        
        Returns:
            Dictionary with model details
        """
        pass
    
    def validate_request(self, request: GenerationRequest) -> Tuple[bool, Optional[str]]:
        """
        Validate generation request parameters.
        
        Args:
            request: Generation request to validate
            
        Returns:
            Tuple of (is_valid, error_message)
        """
        if not request.primary_image:
            return False, "Primary image is required"
        
        if not request.room_images or 'north' not in request.room_images:
            return False, "North direction image is required"
        
        if request.image_strength < 0.1 or request.image_strength > 1.0:
            return False, "Image strength must be between 0.1 and 1.0"
        
        if request.controlnet_weight < 0.5 or request.controlnet_weight > 2.0:
            return False, "ControlNet weight must be between 0.5 and 2.0"
        
        if request.num_inference_steps < 10 or request.num_inference_steps > 100:
            return False, "Inference steps must be between 10 and 100"
        
        return True, None
    
    def prepare_seeds(self, num_variations: int = 3) -> List[int]:
        """
        Generate deterministic seeds for reproducible variations.
        
        Args:
            num_variations: Number of variations to generate
            
        Returns:
            List of seed values
        """
        import random
        if self.config.get('deterministic', True):
            # Use fixed seeds for reproducible results
            base_seeds = [42, 123, 456, 789, 999]
            return base_seeds[:num_variations]
        else:
            return [random.randint(0, 2**32 - 1) for _ in range(num_variations)]


class EngineFactory:
    """
    Factory class for creating AI engine instances based on configuration.
    
    Supports dynamic engine switching via AI_ENGINE environment variable.
    """
    
    _engines = {
        EngineType.LOCAL_SDXL: None,
        EngineType.REPLICATE: None,
        EngineType.HF_INFERENCE: None
    }
    
    @classmethod
    def create_engine(cls, engine_type: EngineType, config: Dict[str, Any]) -> BaseEngine:
        """
        Create an instance of the specified engine type.
        
        Args:
            engine_type: Type of engine to create
            config: Engine configuration
            
        Returns:
            Initialized engine instance
        """
        if engine_type == EngineType.LOCAL_SDXL:
            from .models_lab_engine import ModelsLabEngine
            return ModelsLabEngine(config)
        
        elif engine_type == EngineType.REPLICATE:
            from .replicate_img2img_engine import ReplicateEngine
            return ReplicateEngine(config)
        
        elif engine_type == EngineType.HF_INFERENCE:
            from .hf_img2img_engine import HFEngine
            return HFEngine(config)
        
        elif engine_type == EngineType.HUGGINGFACE:
            from .huggingface_engine import HuggingFaceEngine
            return HuggingFaceEngine(config)
        
        elif engine_type == EngineType.STATE_OF_THE_ART:
            from .state_of_the_art_interior_engine import StateOfTheArtInteriorEngine
            return StateOfTheArtInteriorEngine(config)
        
        elif engine_type == EngineType.POLLINATIONS:
            from .pollinations_engine import PollinationsEngine
            return PollinationsEngine(config)
        
        elif engine_type == EngineType.SD15_CONTROLNET:
            from .simple_sd15_engine import SimpleSD15Engine
            return SimpleSD15Engine(config)
        
        else:
            # Default to Standalone Image Engine for reliable image generation
            from .standalone_image_engine import StandaloneImageEngine
            return StandaloneImageEngine(config)
    
    @classmethod
    def get_engine_from_env(cls) -> BaseEngine:
        """
        Create engine instance based on environment configuration.
        
        Returns:
            Initialized engine instance
        """
        from app.config import get_settings
        settings = get_settings()
        
        engine_str = getattr(settings, 'AI_ENGINE', 'local_sdxl')
        engine_type = EngineType(engine_str)
        
        # Build engine-specific config
        config = {
            'model_path': getattr(settings, 'SDXL_MODEL_PATH', 'stabilityai/stable-diffusion-xl-base-1.0'),
            'controlnet_model': getattr(settings, 'CONTROLNET_MODEL', 'lllyasviel/sd-controlnet-canny'),
            'device': getattr(settings, 'DEVICE', 'cuda' if settings.ENVIRONMENT == 'development' else 'cpu'),
            'replicate_api_token': getattr(settings, 'REPLICATE_API_TOKEN', None),
            'hf_api_key': getattr(settings, 'HF_API_KEY', None),
            'hf_endpoint_url': getattr(settings, 'HF_ENDPOINT_URL', None),
            'max_resolution': getattr(settings, 'MAX_RESOLUTION', (1024, 1024)),
            'timeout_seconds': getattr(settings, 'AI_TIMEOUT_SECONDS', 60),
            'deterministic': getattr(settings, 'DETERMINISTIC_GENERATION', True)
        }
        
        return cls.create_engine(engine_type, config)
