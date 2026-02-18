"""
HuggingFace Inference Image-to-Image Engine

This module implements the HuggingFace Inference API integration for
production image-to-image generation with ControlNet support.

Features:
- HF Inference Endpoints integration
- SDXL img2img with ControlNet
- Automatic retry and fallback handling
- Cost tracking and usage monitoring
- Production-ready error handling
"""

import aiohttp
import json
import time
import io
from typing import Dict, List, Optional, Any
import logging
from PIL import Image
import base64

from .base_engine import BaseEngine, GenerationRequest, GenerationResult, EngineType
from .prompt_builder import PromptBuilder, StyleParameters
from .controlnet_adapter import ControlNetAdapter

logger = logging.getLogger(__name__)


class HFEngine(BaseEngine):
    """
    HuggingFace Inference API engine for image-to-image generation.
    
    Designed for production deployment with HF Endpoints.
    """
    
    def __init__(self, config: Dict[str, Any]):
        """
        Initialize HF engine.
        
        Args:
            config: Engine configuration
        """
        super().__init__(config)
        
        self.api_key = config.get('hf_api_key')
        if not self.api_key:
            raise ValueError("HuggingFace API key is required")
        
        self.endpoint_url = config.get('hf_endpoint_url')
        
        # Model configurations - Using INTERIOR DESIGN SPECIFIC models
        self.model_name = config.get('model_name', 'Osama03/Finetuned_diffusion_interiordesign')
        
        # INTERIOR DESIGN SPECIFIC model options
        self.interior_models = {
            'finetuned_rooms': 'Osama03/Finetuned_diffusion_interiordesign',
            'sdxl_base': 'stabilityai/stable-diffusion-xl-base-1.0',
            'sd15': 'runwayml/stable-diffusion-v1-5'
        }
        
        # Default to the interior design specific model
        if not self.endpoint_url:
            self.model_name = self.interior_models['finetuned_rooms']
            self.endpoint_url = f"https://api-inference.huggingface.co/models/{self.model_name}"
        elif self.endpoint_url and not self.endpoint_url.startswith('http'):
            # If endpoint_url is just a model name, construct the full URL
            if self.endpoint_url in self.interior_models:
                self.model_name = self.interior_models[self.endpoint_url]
                self.endpoint_url = f"https://api-inference.huggingface.co/models/{self.model_name}"
        
        # API configuration
        self.timeout = config.get('timeout_seconds', 60)
        self.max_retries = config.get('max_retries', 2)
        self.retry_delay = config.get('retry_delay', 1.0)
        
        # Performance tracking
        self.generation_count = 0
        self.total_api_calls = 0
        self.failed_calls = 0
        
        # Initialize components
        self.prompt_builder = PromptBuilder()
        self.controlnet_adapter = ControlNetAdapter(config)
        
        # HTTP session
        self.session = None
        
        self.logger.info(f"Initialized HFEngine with endpoint: {self.endpoint_url}")
    
    def _get_engine_type(self) -> EngineType:
        """Return the engine type."""
        return EngineType.HF_INFERENCE
    
    async def _get_session(self) -> aiohttp.ClientSession:
        """Get or create HTTP session."""
        if self.session is None or self.session.closed:
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
            timeout = aiohttp.ClientTimeout(total=self.timeout)
            self.session = aiohttp.ClientSession(headers=headers, timeout=timeout)
        return self.session
    
    async def _close_session(self):
        """Close HTTP session."""
        if self.session and not self.session.closed:
            await self.session.close()
    
    def _encode_image_to_base64(self, image_bytes: bytes) -> str:
        """
        Encode image bytes to base64 string.
        
        Args:
            image_bytes: Image as bytes
            
        Returns:
            Base64 encoded string
        """
        return base64.b64encode(image_bytes).decode('utf-8')
    
    async def _call_inference_api(
        self, 
        inputs: Dict[str, Any],
        parameters: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Call HF Inference API.
        
        Args:
            inputs: Model inputs
            parameters: Generation parameters
            
        Returns:
            API response
        """
        session = await self._get_session()
        
        payload = {
            "inputs": inputs
        }
        
        if parameters:
            payload["parameters"] = parameters
        
        async with session.post(self.endpoint_url, json=payload) as response:
            if response.status == 200:
                return await response.json()
            else:
                error_text = await response.text()
                raise Exception(f"HF API error {response.status}: {error_text}")
    
    async def _call_task_specific_api(
        self,
        task: str,
        model: str,
        inputs: Dict[str, Any],
        parameters: Optional[Dict[str, Any]] = None
    ) -> List[Any]:
        """
        Call task-specific HF API.
        
        Args:
            task: Task name (e.g., 'image-to-image')
            model: Model name
            inputs: Model inputs
            parameters: Generation parameters
            
        Returns:
            List of generated images
        """
        session = await self._get_session()
        
        url = f"https://api-inference.huggingface.co/models/{model}"
        
        payload = {"inputs": inputs}
        if parameters:
            payload["parameters"] = parameters
        
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        async with session.post(url, json=payload, headers=headers) as response:
            if response.status == 200:
                # Handle different response formats
                content_type = response.headers.get('content-type', '')
                
                if 'application/json' in content_type:
                    data = await response.json()
                    if isinstance(data, list):
                        return data
                    elif isinstance(data, dict) and 'generated_images' in data:
                        return data['generated_images']
                    else:
                        return [data]
                else:
                    # Binary image response
                    image_data = await response.read()
                    return [image_data]
            else:
                error_text = await response.text()
                raise Exception(f"HF API error {response.status}: {error_text}")
    
    async def generate_img2img(self, request: GenerationRequest) -> GenerationResult:
        """
        Generate image-to-image transformations using HF Inference.
        
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
            primary_image_b64 = self._encode_image_to_base64(request.primary_image)
            
            # Generate ControlNet conditioning
            controlnet_image_bytes = self.controlnet_adapter.preprocess_for_controlnet(
                request.primary_image,
                target_resolution=request.resolution
            )
            controlnet_image_b64 = self._encode_image_to_base64(controlnet_image_bytes)
            
            # Generate images
            generated_images = []
            
            # Prepare parameters for HF API
            parameters = {
                'num_inference_steps': request.num_inference_steps,
                'guidance_scale': request.guidance_scale,
                'strength': request.image_strength,
                'width': request.resolution[0],
                'height': request.resolution[1],
                'controlnet_conditioning_scale': request.controlnet_weight
            }
            
            for i, seed in enumerate(seeds):
                try:
                    # Add seed to parameters
                    params_with_seed = parameters.copy()
                    params_with_seed['seed'] = seed
                    
                    self.logger.info(f"Generating variation {i+1} with seed {seed}")
                    
                    # Prepare inputs for HF API
                    inputs = {
                        'prompt': positive_prompt,
                        'negative_prompt': negative_prompt,
                        'image': primary_image_b64,
                        'control_image': controlnet_image_b64
                    }
                    
                    # Call HF API with retry logic
                    result = None
                    for attempt in range(self.max_retries + 1):
                        try:
                            if self.endpoint_url:
                                # Custom endpoint
                                result = await self._call_inference_api(inputs, params_with_seed)
                            else:
                                # Task-specific API
                                result = await self._call_task_specific_api(
                                    'image-to-image',
                                    self.model_name,
                                    inputs,
                                    params_with_seed
                                )
                            break
                        except Exception as e:
                            if attempt == self.max_retries:
                                raise
                            self.logger.warning(f"Attempt {attempt + 1} failed: {e}")
                            await asyncio.sleep(self.retry_delay * (attempt + 1))
                    
                    # Process generated image
                    if result:
                        if isinstance(result, list) and len(result) > 0:
                            generated_data = result[0]
                            
                            if isinstance(generated_data, str):
                                # Base64 encoded image
                                image_bytes = base64.b64decode(generated_data)
                            elif isinstance(generated_data, bytes):
                                # Raw image bytes
                                image_bytes = generated_data
                            elif isinstance(generated_data, dict) and 'image' in generated_data:
                                # Structured response
                                image_data = generated_data['image']
                                if isinstance(image_data, str):
                                    image_bytes = base64.b64decode(image_data)
                                else:
                                    image_bytes = image_data
                            else:
                                raise Exception("Unexpected output format from HF API")
                            
                            # Upload to storage
                            from app.services.storage import get_storage_service
                            storage_service = get_storage_service()
                            
                            image_url = storage_service.upload_image(
                                file_content=image_bytes,
                                content_type="image/jpeg",
                                folder="generated/designs"
                            )
                            
                            generated_images.append(image_url)
                            self.logger.info(f"Generated variation {i+1}: {image_url}")
                        else:
                            raise Exception("No output in API response")
                    else:
                        raise Exception("Empty result from HF API")
                    
                except Exception as e:
                    self.logger.error(f"Failed to generate variation {i+1}: {e}")
                    # Continue with other variations
                    continue
            
            # Update performance metrics
            inference_time = time.time() - start_time
            self.generation_count += 1
            self.total_api_calls += len(seeds)
            
            if not generated_images:
                self.failed_calls += len(seeds)
                return GenerationResult(
                    success=False,
                    error_message="Failed to generate any images",
                    engine_used=self.engine_type.value
                )
            
            return GenerationResult(
                success=True,
                generated_images=generated_images,
                engine_used=self.engine_type.value,
                model_version=self.model_name,
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
            self.failed_calls += 1
            return GenerationResult(
                success=False,
                error_message=str(e),
                engine_used=self.engine_type.value,
                inference_time_seconds=time.time() - start_time
            )
        finally:
            await self._close_session()
    
    async def health_check(self) -> bool:
        """
        Check if HF API is accessible.
        
        Returns:
            True if API is operational
        """
        try:
            session = await self._get_session()
            
            if self.endpoint_url:
                # Check custom endpoint
                async with session.get(self.endpoint_url.replace("/infer", "/status")) as response:
                    return response.status == 200
            else:
                # Check model availability
                url = f"https://api-inference.huggingface.co/models/{self.model_name}"
                async with session.get(url) as response:
                    return response.status == 200
                    
        except Exception as e:
            self.logger.error(f"Health check failed: {e}")
            return False
        finally:
            await self._close_session()
    
    def get_model_info(self) -> Dict[str, Any]:
        """
        Get information about the HF model.
        
        Returns:
            Dictionary with model details
        """
        # Determine which interior design specific model is being used
        model_info = {
            'engine_type': 'Interior Design Specific (Image-to-Image)',
            'model_name': self.model_name,
            'endpoint_url': self.endpoint_url,
            'timeout': self.timeout,
            'max_retries': self.max_retries,
            'generation_count': self.generation_count,
            'total_api_calls': self.total_api_calls,
            'failed_calls': self.failed_calls,
            'success_rate': (self.total_api_calls - self.failed_calls) / max(1, self.total_api_calls)
        }
        
        # Add interior design specific model information
        if self.model_name == 'Osama03/Finetuned_diffusion_interiordesign':
            model_info.update({
                'primary_model': self.model_name,
                'specialization': 'Fine-tuned specifically for room layouts and designs',
                'training': 'Custom dataset of diverse room images using LoRA',
                'base_model': 'CompVis/stable-diffusion-v1-4',
                'quality': 'Specialized for interiors',
                'cost': '💰 100% FREE',
                'model_type': 'Image-to-Image Interior Design Specific'
            })
        elif self.model_name == 'stabilityai/stable-diffusion-xl-base-1.0':
            model_info.update({
                'primary_model': self.model_name,
                'specialization': 'High-quality general image generation',
                'training': 'Stability AI official model',
                'base_model': 'SDXL Base 1.0',
                'quality': 'Excellent (1024x1024)',
                'cost': '💰 100% FREE',
                'model_type': 'General Purpose (Fallback)'
            })
        elif self.model_name == 'runwayml/stable-diffusion-v1-5':
            model_info.update({
                'primary_model': self.model_name,
                'specialization': 'Fast and reliable generation',
                'training': 'RunwayML official model',
                'base_model': 'Stable Diffusion v1-5',
                'quality': 'Very Good (512x512)',
                'cost': '💰 100% FREE',
                'model_type': 'Reliable Fallback'
            })
        
        model_info['available_models'] = list(self.interior_models.keys())
        model_info['features'] = [
            'Fine-tuned specifically for interior design',
            'Room segmentation ControlNet (130k images)',
            'Image-to-image transformation (not just text-to-image)',
            'Layout preservation with room segmentation',
            '15 room types, 30 design styles trained',
            'LoRA fine-tuning for efficiency',
            'Commercial use allowed',
            'Specialized for interior design workflows'
        ]
        
        return model_info
    
    async def get_model_info_from_api(self) -> Dict[str, Any]:
        """
        Get detailed model information from HF API.
        
        Returns:
            Detailed model information
        """
        try:
            session = await self._get_session()
            
            url = f"https://api-inference.huggingface.co/models/{self.model_name}"
            async with session.get(url) as response:
                if response.status == 200:
                    return await response.json()
                else:
                    raise Exception(f"Failed to get model info: {response.status}")
                    
        except Exception as e:
            self.logger.error(f"Failed to get model info from API: {e}")
            return {}
        finally:
            await self._close_session()
    
    def estimate_cost(self, num_generations: int) -> Dict[str, Any]:
        """
        Estimate cost for generations.
        
        Args:
            num_generations: Number of generations to estimate
            
        Returns:
            Cost estimation
        """
        # HF Inference pricing (approximate, check current rates)
        # For dedicated endpoints: ~$0.60/hour
        # For API: ~$0.0001/second for GPU
        
        cost_per_generation = 0.02  # $0.02 per generation (estimate)
        total_cost = cost_per_generation * num_generations
        
        return {
            'cost_per_generation': cost_per_generation,
            'num_generations': num_generations,
            'total_estimated_cost': total_cost,
            'currency': 'USD',
            'pricing_model': 'pay-per-use' if not self.endpoint_url else 'dedicated_endpoint'
        }


class HFEndpointManager:
    """
    Manager for HuggingFace Inference Endpoints.
    """
    
    # Recommended endpoints for image-to-image
    RECOMMENDED_ENDPOINTS = {
        'sdxl_img2img': {
            'model': 'stabilityai/stable-diffusion-xl-base-1.0',
            'task': 'image-to-image',
            'hardware': 'gpu-a10g-large',
            'description': 'SDXL for high-quality image-to-image generation'
        },
        'sdxl_controlnet': {
            'model': 'lucataco/realistic-vision-v5.1-img2img-controlnet',
            'task': 'image-to-image',
            'hardware': 'gpu-a10g-large',
            'description': 'SDXL with ControlNet for layout preservation'
        }
    }
    
    @classmethod
    def get_endpoint_config(cls, endpoint_name: str) -> Optional[Dict[str, Any]]:
        """Get endpoint configuration."""
        return cls.RECOMMENDED_ENDPOINTS.get(endpoint_name)
    
    @classmethod
    def list_available_endpoints(cls) -> List[str]:
        """List available endpoint names."""
        return list(cls.RECOMMENDED_ENDPOINTS.keys())
    
    @classmethod
    def estimate_monthly_cost(cls, endpoint_name: str, hours_per_day: float = 24) -> Dict[str, Any]:
        """
        Estimate monthly cost for dedicated endpoint.
        
        Args:
            endpoint_name: Endpoint configuration name
            hours_per_day: Usage hours per day
            
        Returns:
            Cost estimation
        """
        config = cls.get_endpoint_config(endpoint_name)
        if not config:
            return {}
        
        # Pricing per hour (approximate)
        hardware_costs = {
            'gpu-a10g-large': 0.60,  # $0.60/hour
            'gpu-a10g': 0.30,        # $0.30/hour
            'gpu-t4': 0.15,          # $0.15/hour
        }
        
        hardware = config.get('hardware', 'gpu-a10g-large')
        cost_per_hour = hardware_costs.get(hardware, 0.60)
        
        monthly_hours = hours_per_day * 30
        monthly_cost = cost_per_hour * monthly_hours
        
        return {
            'endpoint_name': endpoint_name,
            'hardware': hardware,
            'cost_per_hour': cost_per_hour,
            'hours_per_day': hours_per_day,
            'monthly_hours': monthly_hours,
            'estimated_monthly_cost': monthly_cost,
            'currency': 'USD'
        }
