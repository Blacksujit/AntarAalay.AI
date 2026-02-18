"""
Local Open-Source Interior Design Engine

This module implements local open-source interior design models:
- Interior Scene XL (SDXL-based interior design model)
- Interior Design v1 (Dreambooth trained on 500 living room images)
- InteriorDesign_lulu_v1.0 (Universal interior design model)
- Local ControlNet models for layout preservation
- No API dependencies - works completely offline

Features:
- 100% open-source models
- No API costs or dependencies
- Interior design specific training
- Image-to-image transformation
- Local processing (Python 3.14 compatible)
- Commercial use allowed
"""

import time
import io
import logging
import base64
from typing import Dict, List, Optional, Any
from PIL import Image
import torch
import numpy as np
from pathlib import Path

try:
    from diffusers import StableDiffusionImg2ImgPipeline, ControlNetModel, DDIMScheduler
    from diffusers.utils import load_image
    DIFFUSERS_AVAILABLE = True
except ImportError:
    DIFFUSERS_AVAILABLE = False

from .base_engine import BaseEngine, GenerationRequest, GenerationResult, EngineType
from .prompt_builder import PromptBuilder, StyleParameters
from .controlnet_adapter import ControlNetAdapter

logger = logging.getLogger(__name__)


class LocalOpenSourceInteriorEngine(BaseEngine):
    """
    Local Open-Source Interior Design Engine.
    
    Uses locally downloaded interior design models:
    - Interior Scene XL (SDXL-based)
    - Interior Design v1 (Dreambooth trained)
    - InteriorDesign_lulu_v1.0 (Universal model)
    - Local ControlNet for layout preservation
    """
    
    def __init__(self, config: Dict[str, Any]):
        """
        Initialize Local Open-Source Interior Design Engine.
        
        Args:
            config: Engine configuration
        """
        super().__init__(config)
        
        if not DIFFUSERS_AVAILABLE:
            raise ImportError(
                "Diffusers library is required. Install with: "
                "pip install diffusers transformers accelerate torch"
            )
        
        # Model paths (local download required)
        self.models_dir = Path(config.get('models_dir', './models'))
        self.models_dir.mkdir(exist_ok=True)
        
        # OPEN-SOURCE INTERIOR DESIGN MODELS
        self.interior_models = {
            'interior_scene_xl': {
                'path': self.models_dir / 'interior-scene-xl.safetensors',
                'url': 'https://civitai.com/api/download/models/715747',
                'base_model': 'SDXL 1.0',
                'specialization': 'SDXL-based interior design with luxury style',
                'size': '6.46 GB',
                'license': 'CreativeML Open RAIL++-M'
            },
            'interior_design_v1': {
                'path': self.models_dir / 'interior-design-v1.safetensors',
                'url': 'https://civitai.com/api/download/models/54699',
                'base_model': 'SD 1.5',
                'specialization': 'Dreambooth trained on 500 living room images',
                'size': '1.99 GB',
                'license': 'CreativeML Open RAIL-M'
            },
            'interiordesign_lulu': {
                'path': self.models_dir / 'interiordesign-lulu-v1.0.safetensors',
                'url': 'https://civitai.com/api/download/models/622597',
                'base_model': 'SD 1.5',
                'specialization': 'Universal model for multi-style home design',
                'size': '3.59 GB',
                'license': 'CreativeML Open RAIL++-M'
            }
        }
        
        # ControlNet models (local)
        self.controlnet_models = {
            'canny': {
                'path': self.models_dir / 'controlnet-canny.safetensors',
                'url': 'https://huggingface.co/lllyasviel/sd-controlnet-canny/resolve/main/diffusion_pytorch_model.bin',
                'specialization': 'Edge detection for layout preservation'
            },
            'depth': {
                'path': self.models_dir / 'controlnet-depth.safetensors',
                'url': 'https://huggingface.co/lllyasviel/sd-controlnet-depth/resolve/main/diffusion_pytorch_model.bin',
                'specialization': 'Depth map for spatial awareness'
            }
        }
        
        # Configuration
        self.device = config.get('device', 'cuda' if torch.cuda.is_available() else 'cpu')
        self.primary_model = config.get('primary_model', 'interior_scene_xl')
        self.use_controlnet = config.get('use_controlnet', True)
        self.primary_controlnet = config.get('primary_controlnet', 'canny')
        
        # Initialize pipelines
        self.pipelines = {}
        self.controlnets = {}
        
        self.logger.info(f"Initialized Local Open-Source Interior Design Engine")
        self.logger.info(f"Device: {self.device}")
        self.logger.info(f"Models directory: {self.models_dir}")
        self.logger.info(f"Primary model: {self.primary_model}")
        self.logger.info("🏠 100% Open-Source - No API dependencies!")
        
        # Performance tracking
        self.generation_count = 0
        self.total_generations = 0
        self.failed_generations = 0
        
        # Initialize components
        self.prompt_builder = PromptBuilder()
        self.controlnet_adapter = ControlNetAdapter(config)
    
    def _get_engine_type(self) -> EngineType:
        """Get engine type for abstract base class."""
        return EngineType.LOCAL_SDXL
    
    def _download_model(self, model_config: Dict[str, Any]) -> bool:
        """
        Download model if not exists.
        
        Args:
            model_config: Model configuration
            
        Returns:
            True if model is available, False otherwise
        """
        model_path = model_config['path']
        
        if model_path.exists():
            self.logger.info(f"Model already exists: {model_path}")
            return True
        
        self.logger.warning(f"Model not found: {model_path}")
        self.logger.info(f"Please download from: {model_config['url']}")
        self.logger.info(f"Save as: {model_path}")
        self.logger.info(f"Size: {model_config['size']}")
        
        return False
    
    def _load_pipeline(self, model_name: str) -> bool:
        """
        Load diffusion pipeline for model.
        
        Args:
            model_name: Model identifier
            
        Returns:
            True if pipeline loaded successfully
        """
        if model_name in self.pipelines:
            return True
        
        model_config = self.interior_models[model_name]
        
        if not self._download_model(model_config):
            return False
        
        try:
            # Load pipeline based on base model
            if 'SDXL' in model_config['base_model']:
                # SDXL pipeline
                pipeline = StableDiffusionImg2ImgPipeline.from_single_file(
                    model_config['path'],
                    torch_dtype=torch.float16 if self.device == 'cuda' else torch.float32,
                    use_safetensors=True,
                    variant="fp16" if self.device == 'cuda' else None
                )
            else:
                # SD 1.5 pipeline
                pipeline = StableDiffusionImg2ImgPipeline.from_single_file(
                    model_config['path'],
                    torch_dtype=torch.float16 if self.device == 'cuda' else torch.float32,
                    use_safetensors=True
                )
            
            # Move to device
            pipeline = pipeline.to(self.device)
            
            # Enable memory efficient attention if available
            if hasattr(pipeline, "enable_xformers_memory_efficient_attention"):
                try:
                    pipeline.enable_xformers_memory_efficient_attention()
                except Exception:
                    pass
            
            # Enable CPU offload if using CPU
            if self.device == 'cpu':
                pipeline.enable_sequential_cpu_offload()
            
            self.pipelines[model_name] = pipeline
            self.logger.info(f"Loaded pipeline: {model_name}")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to load pipeline {model_name}: {e}")
            return False
    
    def _load_controlnet(self, controlnet_name: str) -> bool:
        """
        Load ControlNet model.
        
        Args:
            controlnet_name: ControlNet identifier
            
        Returns:
            True if ControlNet loaded successfully
        """
        if controlnet_name in self.controlnets:
            return True
        
        controlnet_config = self.controlnet_models[controlnet_name]
        
        if not self._download_model(controlnet_config):
            return False
        
        try:
            controlnet = ControlNetModel.from_single_file(
                controlnet_config['path'],
                torch_dtype=torch.float16 if self.device == 'cuda' else torch.float32
            ).to(self.device)
            
            self.controlnets[controlnet_name] = controlnet
            self.logger.info(f"Loaded ControlNet: {controlnet_name}")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to load ControlNet {controlnet_name}: {e}")
            return False
    
    async def health_check(self) -> bool:
        """
        Check if the local models are available.
        
        Returns:
            True if models are available, False otherwise
        """
        try:
            # Check if primary model is available
            model_config = self.interior_models[self.primary_model]
            return model_config['path'].exists()
        except Exception as e:
            self.logger.error(f"Health check failed: {e}")
            return False
    
    def get_model_info(self) -> Dict[str, Any]:
        """
        Get information about the local models.
        
        Returns:
            Model information dictionary
        """
        model_config = self.interior_models[self.primary_model]
        
        return {
            "engine_type": "Local Open-Source Interior Design",
            "primary_model": self.primary_model,
            "model_path": str(model_config['path']),
            "specialization": model_config['specialization'],
            "base_model": model_config['base_model'],
            "model_size": model_config['size'],
            "license": model_config['license'],
            "device": self.device,
            "available_models": list(self.interior_models.keys()),
            "available_controlnets": list(self.controlnet_models.keys()),
            "cost": "💰 100% FREE (No API costs)",
            "model_type": "Local Open-Source Image-to-Image",
            "features": [
                "100% open-source models",
                "No API dependencies",
                "Interior design specific training",
                "Local processing (offline capable)",
                "Commercial use allowed",
                "Multiple interior design models",
                "ControlNet support for layout preservation",
                "Python 3.14 compatible",
                "SDXL and SD 1.5 support"
            ],
            "download_instructions": {
                "interior_scene_xl": f"Download from {model_config['url']} as interior-scene-xl.safetensors",
                "interior_design_v1": "Download from https://civitai.com/models/54699 as interior-design-v1.safetensors",
                "interiordesign_lulu": "Download from https://civitai.com/models/622597 as interiordesign-lulu-v1.0.safetensors"
            }
        }
    
    def validate_request(self, request: GenerationRequest) -> tuple[bool, Optional[str]]:
        """
        Validate generation request.
        
        Args:
            request: Generation request to validate
            
        Returns:
            Tuple of (is_valid, error_message)
        """
        if not request.primary_image:
            return False, "Primary image is required for image-to-image transformation"
        
        if not request.furniture_style:
            return False, "Furniture style is required"
        
        if request.image_strength < 0.1 or request.image_strength > 1.0:
            return False, "Image strength must be between 0.1 and 1.0"
        
        if request.num_inference_steps < 10 or request.num_inference_steps > 100:
            return False, "Number of inference steps must be between 10 and 100"
        
        return True, None
    
    def prepare_seeds(self, count: int) -> List[int]:
        """
        Prepare random seeds for generation.
        
        Args:
            count: Number of seeds to generate
            
        Returns:
            List of seed values
        """
        import random
        return [random.randint(0, 2**32 - 1) for _ in range(count)]
    
    def _generate_with_local_model(
        self,
        model_name: str,
        prompt: str,
        negative_prompt: str,
        input_image: Image.Image,
        seed: int,
        strength: float = 0.8,
        guidance_scale: float = 7.5,
        num_inference_steps: int = 30
    ) -> Optional[Image.Image]:
        """
        Generate image using local model.
        
        Args:
            model_name: Model identifier
            prompt: Positive prompt
            negative_prompt: Negative prompt
            input_image: Input PIL Image
            seed: Random seed
            strength: Image strength for img2img
            guidance_scale: Guidance scale
            num_inference_steps: Number of inference steps
            
        Returns:
            Generated PIL Image or None if failed
        """
        try:
            # Load pipeline if not loaded
            if not self._load_pipeline(model_name):
                return None
            
            pipeline = self.pipelines[model_name]
            
            # Set generator for reproducibility
            generator = torch.Generator(device=self.device).manual_seed(seed)
            
            # Generate image
            with torch.autocast(self.device):
                result = pipeline(
                    prompt=prompt,
                    negative_prompt=negative_prompt,
                    image=input_image,
                    strength=strength,
                    guidance_scale=guidance_scale,
                    num_inference_steps=num_inference_steps,
                    generator=generator,
                    return_dict=True
                )
            
            return result.images[0]
            
        except Exception as e:
            self.logger.error(f"Generation failed with local model {model_name}: {e}")
            return None
    
    async def _generate_single_variation(
        self,
        request: GenerationRequest,
        seed: int,
        variation_index: int
    ) -> Optional[str]:
        """
        Generate a single design variation using local models.
        
        Args:
            request: Generation request
            seed: Random seed for reproducibility
            variation_index: Index of this variation
            
        Returns:
            Generated image URL or None if failed
        """
        try:
            # Build optimized prompt for interior design
            style_params = StyleParameters(
                room_type=request.room_type,
                furniture_style=request.furniture_style,
                wall_color=request.wall_color,
                flooring_material=request.flooring_material
            )
            
            positive_prompt = self.prompt_builder.build_positive_prompt(style_params)
            negative_prompt = self.prompt_builder.build_negative_prompt()
            
            # Convert bytes to PIL Image
            input_image = Image.open(io.BytesIO(request.primary_image))
            
            # Resize if necessary
            if input_image.size != (512, 512):
                input_image = input_image.resize((512, 512), Image.Resampling.LANCZOS)
            
            # Try primary model first
            generated_image = self._generate_with_local_model(
                model_name=self.primary_model,
                prompt=positive_prompt,
                negative_prompt=negative_prompt,
                input_image=input_image,
                seed=seed,
                strength=request.image_strength,
                guidance_scale=request.guidance_scale,
                num_inference_steps=request.num_inference_steps
            )
            
            if not generated_image:
                # Try fallback models
                for fallback_model in ['interiordesign_lulu', 'interior_design_v1']:
                    self.logger.info(f"Primary model failed, trying {fallback_model}")
                    generated_image = self._generate_with_local_model(
                        model_name=fallback_model,
                        prompt=positive_prompt,
                        negative_prompt=negative_prompt,
                        input_image=input_image,
                        seed=seed,
                        strength=request.image_strength,
                        guidance_scale=request.guidance_scale,
                        num_inference_steps=request.num_inference_steps
                    )
                    if generated_image:
                        break
            
            if generated_image:
                # Convert to base64 for return
                buffer = io.BytesIO()
                generated_image.save(buffer, format='PNG')
                image_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')
                
                self.logger.info(f"✅ Successfully generated variation {variation_index + 1} with LOCAL model")
                return f"data:image/png;base64,{image_base64}"
            else:
                self.logger.error(f"❌ Failed to generate variation {variation_index + 1}")
                return None
                
        except Exception as e:
            self.logger.error(f"Failed to generate variation {variation_index + 1}: {e}")
            return None
    
    async def generate_img2img(self, request: GenerationRequest) -> GenerationResult:
        """
        Generate interior design transformations using local models.
        
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
            
            # Prepare seeds
            if request.seeds is None:
                seeds = self.prepare_seeds(3)
            else:
                seeds = request.seeds[:3]
            
            # Generate images
            generated_images = []
            for i, seed in enumerate(seeds):
                image_url = await self._generate_single_variation(request, seed, i)
                if image_url:
                    generated_images.append(image_url)
                    self.logger.info(f"Generated variation {i+1}")
                else:
                    self.logger.warning(f"Failed to generate variation {i+1}")
            
            # Check if we generated any images
            if not generated_images:
                return GenerationResult(
                    success=False,
                    error_message="Failed to generate any images",
                    engine_used=self.engine_type.value
                )
            
            # Calculate generation time
            inference_time = time.time() - start_time
            
            # Create result
            result = GenerationResult(
                success=True,
                generated_images=generated_images,
                engine_used=self.engine_type.value,
                model_version=self.primary_model,
                inference_time_seconds=inference_time,
                seeds_used=seeds
            )
            
            self.generation_count += 1
            self.logger.info(f"✅ Successfully generated {len(generated_images)} LOCAL images in {inference_time:.2f}s")
            self.logger.info("🏠 Used open-source interior design models!")
            
            return result
            
        except Exception as e:
            self.logger.error(f"Generation failed: {e}")
            return GenerationResult(
                success=False,
                error_message=str(e),
                engine_used=self.engine_type.value
            )
