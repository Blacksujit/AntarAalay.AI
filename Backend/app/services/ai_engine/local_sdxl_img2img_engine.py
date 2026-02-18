"""
Local SDXL Image-to-Image Engine with ControlNet

This module implements local Stable Diffusion XL with ControlNet for
development and testing purposes.

Features:
- SDXL img2img pipeline with ControlNet conditioning
- GPU acceleration with fallback to CPU
- Canny edge detection for layout preservation
- Configurable generation parameters
- Memory optimization for local deployment
"""

import time
import io
from typing import Dict, List, Optional, Any
import logging
from PIL import Image
import numpy as np

# Optional torch import for local development
try:
    import torch
    TORCH_AVAILABLE = True
except ImportError:
    TORCH_AVAILABLE = False
    torch = None

from .base_engine import BaseEngine, GenerationRequest, GenerationResult, EngineType
from .prompt_builder import PromptBuilder, StyleParameters
from .controlnet_adapter import ControlNetAdapter

logger = logging.getLogger(__name__)


class LocalSDXLEngine(BaseEngine):
    """
    Local Stable Diffusion XL engine with ControlNet support.
    
    Designed for development and testing with local GPU resources.
    """
    
    def __init__(self, config: Dict[str, Any]):
        """
        Initialize local SDXL engine.
        
        Args:
            config: Engine configuration
        """
        if not TORCH_AVAILABLE:
            raise ImportError(
                "PyTorch is required for LocalSDXLEngine. "
                "Install with: pip install torch torchvision diffusers transformers accelerate"
            )
        
        super().__init__(config)
        
        # Model configuration - Using OPEN-SOURCE INTERIOR DESIGN models
        self.model_path = config.get('model_path', './models/interior-scene-xl.safetensors')
        
        # OPEN-SOURCE INTERIOR DESIGN models
        self.interior_models = {
            'interior_scene_xl': {
                'path': './models/interior-scene-xl.safetensors',
                'url': 'https://civitai.com/api/download/models/715747',
                'base_model': 'SDXL 1.0',
                'specialization': 'SDXL-based interior design with luxury style'
            },
            'interior_design_v1': {
                'path': './models/interior-design-v1.safetensors',
                'url': 'https://civitai.com/api/download/models/54699',
                'base_model': 'SD 1.5',
                'specialization': 'Dreambooth trained on 500 living room images'
            },
            'interiordesign_lulu': {
                'path': './models/interiordesign-lulu-v1.0.safetensors',
                'url': 'https://civitai.com/api/download/models/622597',
                'base_model': 'SD 1.5',
                'specialization': 'Universal model for multi-style home design'
            }
        }
        
        self.primary_model = config.get('primary_model', 'interior_scene_xl')
        self.controlnet_model = config.get('controlnet_model', 'lllyasviel/sd-controlnet-canny')
        self.device = config.get('device', 'cuda' if torch.cuda.is_available() else 'cpu')
        self.torch_dtype = torch.float16 if self.device == 'cuda' else torch.float32
        self.enable_attention_slicing = config.get('enable_attention_slicing', True)
        self.enable_cpu_offload = config.get('enable_cpu_offload', self.device == 'cpu')
        
        # Initialize components
        self.pipeline = None
        self.controlnet = None
        self.prompt_builder = PromptBuilder()
        self.controlnet_adapter = ControlNetAdapter(config)
        
        # Performance tracking
        self.generation_count = 0
        self.total_inference_time = 0.0
        
        self.logger.info(f"Initialized LocalSDXLEngine with device: {self.device}")
    
    def _get_engine_type(self) -> EngineType:
        """Return the engine type."""
        return EngineType.LOCAL_SDXL
    
    async def _load_models(self) -> bool:
        """
        Load SDXL and ControlNet models.
        
        Returns:
            True if models loaded successfully
        """
        try:
            from diffusers import StableDiffusionXLImg2ImgPipeline, ControlNetModel
            from diffusers.utils import logging as diffusers_logging
            
            # Suppress diffusers warnings
            diffusers_logging.set_verbosity_error()
            
            self.logger.info("Loading SDXL img2img pipeline...")
            
            # Load ControlNet
            self.logger.info(f"Loading ControlNet: {self.controlnet_model}")
            self.controlnet = ControlNetModel.from_pretrained(
                self.controlnet_model,
                torch_dtype=self.torch_dtype,
                variant="fp16" if self.torch_dtype == torch.float16 else None
            )
            
            # Load SDXL pipeline
            self.logger.info(f"Loading SDXL: {self.model_path}")
            self.pipeline = StableDiffusionXLImg2ImgPipeline.from_pretrained(
                self.model_path,
                controlnet=self.controlnet,
                torch_dtype=self.torch_dtype,
                variant="fp16" if self.torch_dtype == torch.float16 else None,
                use_safetensors=True
            )
            
            # Move to device
            self.pipeline = self.pipeline.to(self.device)
            
            # Memory optimizations
            if self.enable_attention_slicing:
                self.pipeline.enable_attention_slicing()
                self.logger.info("Enabled attention slicing")
            
            if self.enable_cpu_offload:
                self.pipeline.enable_sequential_cpu_offload()
                self.logger.info("Enabled CPU offloading")
            
            # Compile for better performance (PyTorch 2.0+)
            if hasattr(torch, 'compile') and self.device == 'cuda':
                try:
                    self.pipeline.unet = torch.compile(self.pipeline.unet, mode="reduce-overhead")
                    self.logger.info("Compiled UNet for better performance")
                except Exception as e:
                    self.logger.warning(f"Failed to compile UNet: {e}")
            
            self.logger.info("Models loaded successfully")
            return True
            
        except ImportError as e:
            self.logger.error(f"Missing dependencies: {e}")
            self.logger.error("Install with: pip install diffusers transformers accelerate")
            return False
        except Exception as e:
            self.logger.error(f"Failed to load models: {e}")
            return False
    
    async def generate_img2img(self, request: GenerationRequest) -> GenerationResult:
        """
        Generate image-to-image transformations with ControlNet.
        
        Args:
            request: Generation parameters and input images
            
        Returns:
            GenerationResult with URLs to generated images
        """
        start_time = time.time()
        
        try:
            # Validate request
            is_valid, error_msg = self.validate_request(request)
            if not is_valid:
                return GenerationResult(
                    success=False,
                    error_message=error_msg,
                    engine_used=self.engine_type.value
                )
            
            # Load models if not loaded
            if self.pipeline is None:
                if not await self._load_models():
                    return GenerationResult(
                        success=False,
                        error_message="Failed to load AI models",
                        engine_used=self.engine_type.value
                    )
            
            # Prepare style parameters
            style_params = StyleParameters(
                room_type=request.room_type,
                furniture_style=request.furniture_style,
                wall_color=request.wall_color,
                flooring_material=request.flooring_material
            )
            
            # Build prompts
            positive_prompt = self.prompt_builder.build_positive_prompt(style_params)
            negative_prompt = self.prompt_builder.build_negative_prompt()
            
            # Prepare seeds
            if request.seeds is None:
                seeds = self.prepare_seeds(3)
            else:
                seeds = request.seeds[:3]
            
            # Preprocess images
            primary_image = Image.open(io.BytesIO(request.primary_image))
            
            # Generate ControlNet conditioning
            controlnet_image = self.controlnet_adapter.preprocess_for_controlnet(
                request.primary_image,
                target_resolution=request.resolution
            )
            controlnet_image = Image.open(io.BytesIO(controlnet_image))
            
            # Generate images
            generated_images = []
            generation_params = {
                'prompt': positive_prompt,
                'negative_prompt': negative_prompt,
                'image': primary_image,
                'control_image': controlnet_image,
                'controlnet_conditioning_scale': request.controlnet_weight,
                'num_inference_steps': request.num_inference_steps,
                'guidance_scale': request.guidance_scale,
                'strength': request.image_strength,
                'width': request.resolution[0],
                'height': request.resolution[1],
                'generator': None  # Will be set per seed
            }
            
            for i, seed in enumerate(seeds):
                try:
                    # Set generator for reproducible results
                    generator = torch.Generator(device=self.device).manual_seed(seed)
                    generation_params['generator'] = generator
                    
                    self.logger.info(f"Generating variation {i+1} with seed {seed}")
                    
                    # Generate image
                    with torch.autocast(self.device):
                        result = self.pipeline(**generation_params)
                        generated_image = result.images[0]
                    
                    # Convert to bytes
                    buffer = io.BytesIO()
                    generated_image.save(buffer, format='JPEG', quality=90)
                    image_bytes = buffer.getvalue()
                    
                    # Upload to storage (using existing storage service)
                    from app.services.storage import get_storage_service
                    storage_service = get_storage_service()
                    
                    image_url = storage_service.upload_image(
                        file_content=image_bytes,
                        content_type="image/jpeg",
                        folder="generated/designs"
                    )
                    
                    generated_images.append(image_url)
                    self.logger.info(f"Generated variation {i+1}: {image_url}")
                    
                except Exception as e:
                    self.logger.error(f"Failed to generate variation {i+1}: {e}")
                    # Continue with other variations
                    continue
            
            # Update performance metrics
            inference_time = time.time() - start_time
            self.generation_count += 1
            self.total_inference_time += inference_time
            
            if not generated_images:
                return GenerationResult(
                    success=False,
                    error_message="Failed to generate any images",
                    engine_used=self.engine_type.value
                )
            
            return GenerationResult(
                success=True,
                generated_images=generated_images,
                engine_used=self.engine_type.value,
                model_version=self.model_path,
                generation_params={
                    'controlnet_weight': request.controlnet_weight,
                    'image_strength': request.image_strength,
                    'num_inference_steps': request.num_inference_steps,
                    'guidance_scale': request.guidance_scale,
                    'resolution': request.resolution
                },
                seeds_used=seeds,
                inference_time_seconds=inference_time
            )
            
        except Exception as e:
            self.logger.error(f"Generation failed: {e}")
            return GenerationResult(
                success=False,
                error_message=str(e),
                engine_used=self.engine_type.value,
                inference_time_seconds=time.time() - start_time
            )
    
    async def health_check(self) -> bool:
        """
        Check if the engine is available and healthy.
        
        Returns:
            True if engine is operational
        """
        try:
            if self.pipeline is None:
                return await self._load_models()
            
            # Test with minimal generation
            test_image = Image.new('RGB', (64, 64), color='white')
            test_prompt = "test"
            
            # Quick test without actual generation
            return self.pipeline is not None and self.controlnet is not None
            
        except Exception as e:
            self.logger.error(f"Health check failed: {e}")
            return False
    
    def get_model_info(self) -> Dict[str, Any]:
        """
        Get information about the loaded model.
        
        Returns:
            Dictionary with model details
        """
        info = {
            'engine_type': self.engine_type.value,
            'model_path': self.model_path,
            'controlnet_model': self.controlnet_model,
            'device': self.device,
            'torch_dtype': str(self.torch_dtype),
            'models_loaded': self.pipeline is not None,
            'generation_count': self.generation_count,
            'avg_inference_time': self.total_inference_time / max(1, self.generation_count)
        }
        
        if torch.cuda.is_available():
            info.update({
                'cuda_available': True,
                'cuda_device_count': torch.cuda.device_count(),
                'cuda_current_device': torch.cuda.current_device(),
                'cuda_memory_allocated': torch.cuda.memory_allocated(),
                'cuda_memory_reserved': torch.cuda.memory_reserved()
            })
        else:
            info['cuda_available'] = False
        
        return info
    
    def unload_models(self):
        """Unload models to free memory."""
        try:
            if self.pipeline is not None:
                del self.pipeline
                self.pipeline = None
            
            if self.controlnet is not None:
                del self.controlnet
                self.controlnet = None
            
            if torch.cuda.is_available():
                torch.cuda.empty_cache()
            
            self.logger.info("Models unloaded from memory")
            
        except Exception as e:
            self.logger.error(f"Error unloading models: {e}")
    
    def get_optimal_batch_size(self) -> int:
        """
        Get optimal batch size based on available memory.
        
        Returns:
            Recommended batch size
        """
        if self.device == 'cpu':
            return 1
        
        if not torch.cuda.is_available():
            return 1
        
        # Get GPU memory
        gpu_memory = torch.cuda.get_device_properties(0).total_memory
        gpu_memory_gb = gpu_memory / (1024**3)
        
        if gpu_memory_gb < 8:
            return 1
        elif gpu_memory_gb < 16:
            return 2
        else:
            return 3
    
    def optimize_for_performance(self):
        """Apply performance optimizations."""
        if self.pipeline is None:
            return
        
        try:
            # Enable memory efficient attention
            if hasattr(self.pipeline, 'enable_xformers_memory_efficient_attention'):
                try:
                    self.pipeline.enable_xformers_memory_efficient_attention()
                    self.logger.info("Enabled xformers memory efficient attention")
                except Exception as e:
                    self.logger.warning(f"Failed to enable xformers: {e}")
            
            # Enable VAE slicing to reduce memory usage
            if hasattr(self.pipeline, 'enable_vae_slicing'):
                self.pipeline.enable_vae_slicing()
                self.logger.info("Enabled VAE slicing")
            
            # Enable VAE tiling for large images
            if hasattr(self.pipeline, 'enable_vae_tiling'):
                self.pipeline.enable_vae_tiling()
                self.logger.info("Enabled VAE tiling")
            
        except Exception as e:
            self.logger.warning(f"Performance optimization failed: {e}")


class LocalSDXLEngineFactory:
    """Factory for creating and managing LocalSDXLEngine instances."""
    
    _instance = None
    
    @classmethod
    def get_instance(cls, config: Dict[str, Any]) -> LocalSDXLEngine:
        """Get singleton engine instance."""
        if cls._instance is None:
            cls._instance = LocalSDXLEngine(config)
        return cls._instance
    
    @classmethod
    def reset_instance(cls):
        """Reset the singleton instance."""
        if cls._instance is not None:
            cls._instance.unload_models()
        cls._instance = None
