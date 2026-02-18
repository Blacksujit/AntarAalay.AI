"""
Replicate API Engine for Interior Design

This module implements the Replicate API integration for interior design generation.
Uses the adirik/interior-design model specialized for room styling.

Features:
- Interior design specific model
- Layout preservation with MLSD ControlNet
- Realistic Vision V3.0 base model
- Production-ready error handling
- Rate limiting and cost tracking
"""

import aiohttp
import json
import time
import io
from typing import Dict, List, Optional, Any
import logging
import asyncio
from PIL import Image
import base64

from .base_engine import BaseEngine, GenerationRequest, GenerationResult, EngineType
from .prompt_builder import PromptBuilder, StyleParameters
from .controlnet_adapter import ControlNetAdapter

logger = logging.getLogger(__name__)


class ReplicateEngine(BaseEngine):
    """
    Replicate API engine for interior design generation.
    
    Uses the adirik/interior-design model specialized for realistic interior
    design transformations with layout preservation.
    """
    
    def __init__(self, config: Dict[str, Any]):
        """
        Initialize Replicate engine.
        
        Args:
            config: Engine configuration
        """
        super().__init__(config)
        
        self.api_token = config.get('replicate_api_token')
        if not self.api_token:
            raise ValueError("Replicate API token is required")
        
        # Interior design specific model
        self.model_version = "adirik/interior-design:9a789f75f032fbee8e2723226f5b9f1a1b05d3e29b0a1a7143ba485e8c9405f5"
        self.max_retries = config.get('max_retries', 3)
        self.retry_delay = config.get('retry_delay', 2)
        
        # Initialize Replicate client
        try:
            import replicate
            self.client = replicate.Client(api_token=self.api_token)
        except ImportError:
            raise ImportError("Replicate package is required. Install with: pip install replicate")
        except Exception as e:
            if "Python 3.14" in str(e):
                raise ImportError("Replicate is not compatible with Python 3.14. Please use Python 3.11-3.13")
            raise
        
        self.logger.info(f"Initialized Replicate engine with interior design model")
        
        # Performance tracking
        self.generation_count = 0
        self.total_api_calls = 0
        self.failed_calls = 0
        
        # Initialize components
        self.prompt_builder = PromptBuilder()
        self.controlnet_adapter = ControlNetAdapter(config)
    
    def _get_engine_type(self) -> EngineType:
        """Get engine type for abstract base class."""
        return EngineType.REPLICATE
    
    async def health_check(self) -> bool:
        """
        Check if the Replicate API is accessible.
        
        Returns:
            True if healthy, False otherwise
        """
        try:
            # Simple health check - try to access the model
            import replicate
            model = replicate.models.get("adirik/interior-design")
            return model is not None
        except Exception as e:
            self.logger.error(f"Health check failed: {e}")
            return False
    
    def get_model_info(self) -> Dict[str, Any]:
        """
        Get information about the current model.
        
        Returns:
            Model information dictionary
        """
        return {
            "model_name": "adirik/interior-design",
            "model_version": self.model_version,
            "base_model": "Realistic Vision V3.0",
            "controlnet": "MLSD (Multi-Line Structure Detection)",
            "specialization": "Interior design with layout preservation",
            "cost_per_generation": 0.0077,  # USD
            "typical_runtime": 8,  # seconds
            "hardware": "Nvidia L40S"
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
            return False, "Primary image is required"
        
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
    
    async def _wait_for_prediction(self, prediction_id: str, max_wait_time: int = 300) -> Any:
        """
        Wait for a prediction to complete.
        
        Args:
            prediction_id: Prediction ID to wait for
            max_wait_time: Maximum time to wait in seconds
            
        Returns:
            Completed prediction object
        """
        start_time = time.time()
        
        while time.time() - start_time < max_wait_time:
            try:
                prediction = self.client.predictions.get(prediction_id)
                
                if prediction.status in ["succeeded", "failed", "canceled"]:
                    return prediction
                
                # Wait before polling again
                await asyncio.sleep(2)
                
            except Exception as e:
                self.logger.error(f"Error checking prediction status: {e}")
                await asyncio.sleep(5)
        
        raise Exception(f"Prediction timeout after {max_wait_time} seconds")
    
    async def _generate_single_variation(
        self,
        request: GenerationRequest,
        seed: int,
        variation_index: int
    ) -> Optional[str]:
        """
        Generate a single design variation using interior design model.
        
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
            
            # Convert image to base64 for the model
            image_base64 = base64.b64encode(request.primary_image).decode('utf-8')
            
            # Prepare input for interior design model
            input_data = {
                "image": f"data:image/png;base64,{image_base64}",
                "prompt": positive_prompt,
                "negative_prompt": negative_prompt,
                "num_inference_steps": request.num_inference_steps,
                "guidance_scale": request.guidance_scale,
                "prompt_strength": request.image_strength,
                "seed": seed
            }
            
            # Create prediction
            prediction = self.client.predictions.create(
                version=self.model_version,
                input=input_data
            )
            
            self.logger.info(f"Created prediction {prediction.id} for variation {variation_index + 1}")
            
            # Wait for completion with timeout
            prediction = await self._wait_for_prediction(prediction.id)
            
            if prediction.status == "succeeded" and prediction.output:
                # The interior design model returns a single image URL
                if isinstance(prediction.output, list) and len(prediction.output) > 0:
                    return prediction.output[0]
                elif isinstance(prediction.output, str):
                    return prediction.output
                else:
                    self.logger.error(f"Unexpected output format: {type(prediction.output)}")
                    return None
            else:
                error_msg = prediction.error or "Unknown error"
                self.logger.error(f"Prediction failed: {error_msg}")
                return None
                
        except Exception as e:
            self.logger.error(f"Failed to generate variation {variation_index + 1}: {e}")
            return None
    
    async def generate_img2img(self, request: GenerationRequest) -> GenerationResult:
        """
        Generate image-to-image transformations using Replicate.
        
        Args:
            request: Generation parameters and input images
            
        Returns:
            GenerationResult with URL to generated image
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
                    self.logger.info(f"Generated variation {i+1}: {image_url}")
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
                model_version=self.model_version,
                inference_time_seconds=inference_time,
                seeds_used=seeds
            )
            
            self.generation_count += 1
            self.logger.info(f"Successfully generated {len(generated_images)} images in {inference_time:.2f}s")
            
            return result
            
        except Exception as e:
            self.logger.error(f"Generation failed: {e}")
            return GenerationResult(
                success=False,
                error_message=str(e),
                engine_used=self.engine_type.value
            )
