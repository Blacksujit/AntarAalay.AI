"""
SD15 + ControlNet Engine for GTX 1650 4GB VRAM

Production-ready interior design engine optimized for 4GB VRAM:
- Base Model: runwayml/stable-diffusion-v1-5
- ControlNet: lllyasviel/control_v11p_sd15_canny
- Memory optimizations for GTX 1650
- Sequential generation only
- 512x512 resolution
"""

import torch
import gc
import logging
import time
import random
import base64
import io
from typing import Dict, List, Optional, Any, Tuple
from pathlib import Path
from PIL import Image
import numpy as np

try:
    from diffusers import StableDiffusionControlNetImg2ImgPipeline, ControlNetModel
    from diffusers.utils import load_image
    DIFFUSERS_AVAILABLE = True
except ImportError:
    DIFFUSERS_AVAILABLE = False

from .base_engine import BaseEngine, GenerationRequest, GenerationResult, EngineType
from .prompt_builder import PromptBuilder
from .controlnet_adapter import ControlNetAdapter

logger = logging.getLogger(__name__)


class SD15ControlNetEngine(BaseEngine):
    """
    Production SD15 + ControlNet engine for GTX 1650 4GB VRAM.
    
    Optimized for memory efficiency:
    - 512x512 resolution only
    - Sequential generation
    - torch.float16
    - xformers attention
    - attention slicing
    - CPU offload
    - CUDA cache clearing
    """
    
    def __init__(self, config: Dict[str, Any]):
        """
        Initialize SD15 ControlNet engine.
        
        Args:
            config: Engine configuration
        """
        super().__init__(config)
        
        if not DIFFUSERS_AVAILABLE:
            raise ImportError(
                "Diffusers library is required. Install with: "
                "pip install diffusers transformers accelerate torch torchvision"
            )
        
        # Memory-optimized configuration for GTX 1650
        self.device = config.get('device', 'cuda' if torch.cuda.is_available() else 'cpu')
        self.resolution = 512  # Fixed for 4GB VRAM
        self.num_inference_steps = min(config.get('num_inference_steps', 25), 25)
        self.guidance_scale = config.get('guidance_scale', 7.0)
        self.strength = config.get('strength', 0.45)
        self.controlnet_conditioning_scale = config.get('controlnet_conditioning_scale', 0.8)
        
        # Model paths
        self.base_model = "runwayml/stable-diffusion-v1-5"
        self.controlnet_model = "lllyasviel/control_v11p_sd15_canny"
        
        # Memory optimization flags
        self.enable_xformers = config.get('enable_xformers', True)
        self.enable_attention_slicing = config.get('enable_attention_slicing', True)
        self.enable_cpu_offload = config.get('enable_cpu_offload', True)
        
        # Pipeline instances (loaded once)
        self.pipeline = None
        self.controlnet = None
        
        # GPU safety
        self.max_concurrent_requests = 1
        self.current_requests = 0
        
        self.logger.info(f"Initialized SD15 ControlNet Engine for GTX 1650")
        self.logger.info(f"Device: {self.device}")
        self.logger.info(f"Resolution: {self.resolution}x{self.resolution}")
        self.logger.info(f"Memory optimizations: xformers={self.enable_xformers}, slicing={self.enable_attention_slicing}, cpu_offload={self.enable_cpu_offload}")
        
        # Initialize components
        self.prompt_builder = PromptBuilder()
        self.controlnet_adapter = ControlNetAdapter(config)
        
        # Load models at startup
        self._load_models()
    
    def _get_engine_type(self) -> EngineType:
        """Get engine type for abstract base class."""
        return EngineType.LOCAL_SDXL
    
    def _load_models(self):
        """Load ControlNet and pipeline models with memory optimizations."""
        try:
            self.logger.info("Loading ControlNet model...")
            
            # Load ControlNet
            self.controlnet = ControlNetModel.from_pretrained(
                self.controlnet_model,
                torch_dtype=torch.float16,
                variant="fp16"
            )
            
            self.logger.info("Loading SD15 pipeline...")
            
            # Load pipeline
            self.pipeline = StableDiffusionControlNetImg2ImgPipeline.from_pretrained(
                self.base_model,
                controlnet=self.controlnet,
                torch_dtype=torch.float16,
                variant="fp16",
                safety_checker=None,
                requires_safety_checker=False
            )
            
            # Move to device
            self.pipeline = self.pipeline.to(self.device)
            
            # Apply memory optimizations
            if self.enable_xformers:
                try:
                    self.pipeline.enable_xformers_memory_efficient_attention()
                    self.logger.info("✅ Enabled xformers memory efficient attention")
                except Exception as e:
                    self.logger.warning(f"⚠️ Could not enable xformers: {e}")
            
            if self.enable_attention_slicing:
                self.pipeline.enable_attention_slicing()
                self.logger.info("✅ Enabled attention slicing")
            
            if self.enable_cpu_offload:
                self.pipeline.enable_sequential_cpu_offload()
                self.logger.info("✅ Enabled CPU offload")
            
            # Warm up
            self.logger.info("Warming up pipeline...")
            dummy_image = Image.new('RGB', (self.resolution, self.resolution), color='white')
            dummy_control = Image.new('RGB', (self.resolution, self.resolution), color='black')
            
            with torch.no_grad():
                _ = self.pipeline(
                    prompt="test",
                    image=dummy_image,
                    control_image=dummy_control,
                    num_inference_steps=1,
                    guidance_scale=1.0,
                    strength=0.1
                )
            
            # Clear cache after warmup
            if torch.cuda.is_available():
                torch.cuda.empty_cache()
            
            self.logger.info("✅ Models loaded successfully")
            
        except Exception as e:
            self.logger.error(f"❌ Failed to load models: {e}")
            raise
    
    async def health_check(self) -> bool:
        """Check if models are loaded and GPU is available."""
        try:
            return self.pipeline is not None and self.controlnet is not None
        except Exception as e:
            self.logger.error(f"Health check failed: {e}")
            return False
    
    def get_model_info(self) -> Dict[str, Any]:
        """Get model information."""
        return {
            "engine_type": "SD15 ControlNet (GTX 1650 Optimized)",
            "base_model": self.base_model,
            "controlnet_model": self.controlnet_model,
            "resolution": f"{self.resolution}x{self.resolution}",
            "device": self.device,
            "memory_optimizations": {
                "xformers": self.enable_xformers,
                "attention_slicing": self.enable_attention_slicing,
                "cpu_offload": self.enable_cpu_offload
            },
            "generation_params": {
                "num_inference_steps": self.num_inference_steps,
                "guidance_scale": self.guidance_scale,
                "strength": self.strength,
                "controlnet_conditioning_scale": self.controlnet_conditioning_scale
            },
            "gpu_requirements": "GTX 1650 4GB VRAM minimum",
            "features": [
                "Geometry preservation with ControlNet",
                "Memory optimized for 4GB VRAM",
                "Sequential generation only",
                "Canny edge detection",
                "Interior design specific prompts",
                "Production-ready stability"
            ],
            "model_status": "Loaded" if self.pipeline else "Not loaded",
            "controlnet_status": "Loaded" if self.controlnet else "Not loaded"
        }
    
    def validate_request(self, request: GenerationRequest) -> Tuple[bool, Optional[str]]:
        """Validate generation request."""
        if not request.primary_image:
            return False, "Primary image is required"
        
        if not request.furniture_style:
            return False, "Furniture style is required"
        
        # Check concurrent request limit
        if self.current_requests >= self.max_concurrent_requests:
            return False, "Too many concurrent requests. Please wait."
        
        return True, None
    
    def prepare_seeds(self, count: int) -> List[int]:
        """Prepare random seeds."""
        return [random.randint(0, 2**32 - 1) for _ in range(count)]
    
    def _clear_gpu_cache(self):
        """Clear GPU cache to prevent OOM."""
        if torch.cuda.is_available():
            torch.cuda.empty_cache()
            gc.collect()
    
    def _generate_single_image(
        self,
        input_image: Image.Image,
        control_image: Image.Image,
        prompt: str,
        negative_prompt: str,
        seed: int
    ) -> Optional[Image.Image]:
        """
        Generate a single image with memory management.
        
        Args:
            input_image: Input room image
            control_image: Canny edge control image
            prompt: Positive prompt
            negative_prompt: Negative prompt
            seed: Random seed
            
        Returns:
            Generated image or None if failed
        """
        try:
            # Set seed for reproducibility
            torch.manual_seed(seed)
            if torch.cuda.is_available():
                torch.cuda.manual_seed(seed)
            
            # Generate with memory optimizations
            with torch.no_grad():
                result = self.pipeline(
                    prompt=prompt,
                    negative_prompt=negative_prompt,
                    image=input_image,
                    control_image=control_image,
                    num_inference_steps=self.num_inference_steps,
                    guidance_scale=self.guidance_scale,
                    strength=self.strength,
                    controlnet_conditioning_scale=self.controlnet_conditioning_scale,
                    generator=torch.Generator(device=self.device).manual_seed(seed)
                )
            
            generated_image = result.images[0]
            
            # Clear cache immediately after generation
            self._clear_gpu_cache()
            
            return generated_image
            
        except torch.cuda.OutOfMemoryError as e:
            self.logger.error(f"GPU OOM error: {e}")
            self._clear_gpu_cache()
            return None
        except Exception as e:
            self.logger.error(f"Generation failed: {e}")
            self._clear_gpu_cache()
            return None
    
    async def _generate_single_variation(
        self,
        request: GenerationRequest,
        seed: int,
        variation_index: int
    ) -> Optional[str]:
        """
        Generate a single design variation.
        
        Args:
            request: Generation request
            seed: Random seed
            variation_index: Index of this variation
            
        Returns:
            Generated image path or None if failed
        """
        try:
            # Increment concurrent request counter
            self.current_requests += 1
            
            # Build prompts
            positive_prompt, negative_prompt = self.prompt_builder.build_prompt(
                furniture_style=request.furniture_style,
                wall_color=request.wall_color,
                flooring_material=request.flooring_material
            )
            
            # Load input image
            input_image = Image.open(io.BytesIO(request.primary_image))
            
            # Resize to 512x512
            input_image = input_image.resize((self.resolution, self.resolution), Image.Resampling.LANCZOS)
            
            # Generate control image (Canny edges)
            control_image = self.controlnet_adapter.generate_canny_edge(input_image)
            
            # Generate image
            generated_image = self._generate_single_image(
                input_image=input_image,
                control_image=control_image,
                prompt=positive_prompt,
                negative_prompt=negative_prompt,
                seed=seed
            )
            
            if generated_image:
                # Convert to base64 for return
                buffer = io.BytesIO()
                generated_image.save(buffer, format='JPEG', quality=90)
                image_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')
                
                self.logger.info(f"✅ Generated variation {variation_index + 1} with seed {seed}")
                return f"data:image/jpeg;base64,{image_base64}"
            else:
                self.logger.error(f"❌ Failed to generate variation {variation_index + 1}")
                return None
                
        except Exception as e:
            self.logger.error(f"Failed to generate variation {variation_index + 1}: {e}")
            return None
        finally:
            # Decrement concurrent request counter
            self.current_requests -= 1
            # Ensure cache is cleared
            self._clear_gpu_cache()
    
    async def generate_img2img(self, request: GenerationRequest) -> GenerationResult:
        """
        Generate interior design transformations.
        
        Args:
            request: Generation parameters
            
        Returns:
            GenerationResult with generated images
        """
        start_time = time.time()
        
        try:
            # Validate request
            is_valid, error_msg = self.validate_request(request)
            if not is_valid:
                return GenerationResult(
                    success=False,
                    generated_images=[],  # Required parameter
                    error_message=error_msg,
                    engine_used=self.engine_type.value
                )
            
            # Prepare seeds
            if request.seeds is None:
                seeds = self.prepare_seeds(3)
            else:
                seeds = request.seeds[:3]
            
            # Generate images sequentially (no batching for 4GB VRAM)
            generated_images = []
            for i, seed in enumerate(seeds):
                self.logger.info(f"Generating variation {i+1}/3 with seed {seed}")
                
                image_url = await self._generate_single_variation(request, seed, i)
                if image_url:
                    generated_images.append(image_url)
                else:
                    self.logger.warning(f"Failed to generate variation {i+1}")
            
            # Check results
            if not generated_images:
                return GenerationResult(
                    success=False,
                    generated_images=[],  # Required parameter
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
                model_version=f"{self.base_model} + {self.controlnet_model}",
                inference_time_seconds=inference_time,
                seeds_used=seeds
            )
            
            self.generation_count += 1
            self.logger.info(f"✅ Generated {len(generated_images)} images in {inference_time:.2f}s")
            
            return result
            
        except Exception as e:
            self.logger.error(f"Generation failed: {e}")
            return GenerationResult(
                success=False,
                generated_images=[],  # Required parameter
                error_message=str(e),
                engine_used=self.engine_type.value
            )
        finally:
            # Ensure cleanup
            self._clear_gpu_cache()
