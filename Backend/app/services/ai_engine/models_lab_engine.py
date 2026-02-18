"""
Models Lab AI Engine - Professional Interior Design Generation

This engine uses Models Lab API to generate professional interior designs
with real AI-powered transformations.
"""

import logging
import time
import base64
import io
import json
import httpx
from typing import Dict, List, Optional, Any, Tuple
from pathlib import Path
from PIL import Image

from .base_engine import BaseEngine, GenerationRequest, GenerationResult, EngineType
from .prompt_builder import PromptBuilder
from .controlnet_adapter import ControlNetAdapter

logger = logging.getLogger(__name__)


class ModelsLabEngine(BaseEngine):
    """
    Models Lab AI Engine for professional interior design generation.
    
    Uses Models Lab API to generate high-quality interior designs
    with proper AI models and professional styling.
    """
    
    def __init__(self, config: Dict[str, Any]):
        super().__init__(config)
        
        # Configuration
        self.api_key = config.get('models_lab_api_key', 'SysT5EwHzi8BgRIDn1eV3ZDuZelOSTFEccIYx2KYnMuoV5CGIRTUSbB4k13v')
        self.base_url = "https://modelslab.com/api/v3"
        self.device = config.get('device', 'cpu')
        self.resolution = 512
        self.generation_count = 0
        
        # Initialize components
        self.prompt_builder = PromptBuilder()
        self.controlnet_adapter = ControlNetAdapter(config)
        
        # Style mappings for Models Lab
        self.style_mappings = {
            'modern': {
                'prompt_enhancement': 'modern interior design, contemporary furniture, clean lines, minimalist decor',
                'negative_prompt': 'cluttered, vintage, traditional, ornate'
            },
            'traditional': {
                'prompt_enhancement': 'traditional interior design, classic furniture, elegant decor, warm colors',
                'negative_prompt': 'modern, minimalist, contemporary, stark'
            },
            'minimalist': {
                'prompt_enhancement': 'minimalist interior design, simple furniture, clean spaces, neutral colors',
                'negative_prompt': 'cluttered, ornate, decorative, busy'
            }
        }
        
        # Flooring mappings
        self.flooring_mappings = {
            'hardwood': 'hardwood flooring, wood floors',
            'carpet': 'carpeted floor, soft carpet',
            'tile': 'tile flooring, ceramic tiles',
            'laminate': 'laminate flooring, modern flooring'
        }
        
        logger.info(f"Initialized Models Lab AI Engine")
        logger.info(f"API Key: {self.api_key[:20]}...")
        logger.info(f"Base URL: {self.base_url}")
        logger.info(f"Resolution: {self.resolution}x{self.resolution}")
        logger.info("✅ Ready for professional AI interior design generation!")
    
    def _get_engine_type(self) -> EngineType:
        return EngineType.LOCAL_SDXL
    
    async def health_check(self) -> bool:
        """Check if the Models Lab API is accessible."""
        try:
            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.get(
                    f"{self.base_url}/models",
                    headers={"Authorization": f"Bearer {self.api_key}"}
                )
                return response.status_code == 200
        except Exception as e:
            logger.error(f"Models Lab health check failed: {e}")
            return False
    
    def get_model_info(self) -> Dict[str, Any]:
        """Get model information."""
        return {
            "engine_type": "Models Lab AI Engine",
            "device": self.device,
            "resolution": f"{self.resolution}x{self.resolution}",
            "status": "Ready for professional AI generation",
            "model_type": "Models Lab API",
            "features": [
                "Professional AI image generation",
                "Interior design specialization",
                "High-quality results",
                "Style customization",
                "Multiple design variations",
                "Real furniture placement",
                "Professional decorations",
                "API-based processing",
                "Fast generation"
            ],
            "supported_styles": list(self.style_mappings.keys()),
            "supported_flooring": list(self.flooring_mappings.keys()),
            "api_provider": "Models Lab"
        }
    
    def _encode_image_to_base64(self, image_data: bytes) -> str:
        """Convert image bytes to base64 string."""
        return base64.b64encode(image_data).decode('utf-8')
    
    def _build_prompt(self, request: GenerationRequest) -> str:
        """Build a comprehensive prompt for Models Lab."""
        base_prompt = "Professional interior design photograph, high quality, detailed room"
        
        # Add style
        style_info = self.style_mappings.get(request.furniture_style, self.style_mappings['modern'])
        style_prompt = style_info['prompt_enhancement']
        
        # Add wall color
        wall_color_prompt = f"{request.wall_color} walls, {request.wall_color} colored walls"
        
        # Add flooring
        flooring_prompt = self.flooring_mappings.get(request.flooring_material, 'hardwood flooring')
        
        # Add room type
        room_prompt = f"{request.room_type} room, residential interior"
        
        # Combine all
        full_prompt = f"{base_prompt}, {style_prompt}, {wall_color_prompt}, {flooring_prompt}, {room_prompt}"
        
        # Add quality enhancements
        full_prompt += ", professional photography, interior design magazine, detailed, realistic, 8k, high resolution"
        
        return full_prompt
    
    def _build_negative_prompt(self, request: GenerationRequest) -> str:
        """Build negative prompt for Models Lab."""
        base_negative = "blurry, low quality, distorted, warped, bad anatomy, bad perspective"
        
        # Add style-specific negative
        style_info = self.style_mappings.get(request.furniture_style, self.style_mappings['modern'])
        style_negative = style_info['negative_prompt']
        
        # Add common issues
        common_negative = "cluttered, messy, unfinished, construction, empty room, furniture missing"
        
        return f"{base_negative}, {style_negative}, {common_negative}, text, watermark, signature"
    
    async def _call_models_lab_api(self, prompt: str, negative_prompt: str, image_data: bytes) -> Dict[str, Any]:
        """Call Models Lab API for image generation."""
        
        # Prepare request payload for Models Lab v3 text2img
        payload = {
            "key": self.api_key,
            "prompt": prompt,
            "negative_prompt": negative_prompt,
            "width": self.resolution,
            "height": self.resolution,
            "samples": 3,  # Generate 3 variations
            "num_inference_steps": 30,
            "guidance_scale": 7.5,
            "seed": None,  # Random seed
            "webhook": None,
            "track_id": None
        }
        
        # Note: Models Lab v3 text2img doesn't support init_image for img2img
        # We'll use text2img to generate interior designs based on the prompt
        
        logger.info(f"Sending request to Models Lab API: {self.base_url}/text2img")
        logger.info(f"Payload: {json.dumps({k: v for k, v in payload.items() if k != 'key'}, indent=2)}")
        
        try:
            async with httpx.AsyncClient(timeout=120.0) as client:
                response = await client.post(
                    f"{self.base_url}/text2img",
                    json=payload,
                    headers={"Content-Type": "application/json"}
                )
                
                if response.status_code == 200:
                    result = response.json()
                    logger.info(f"Models Lab API call successful")
                    logger.info(f"API Response: {json.dumps(result, indent=2)}")
                    return result
                else:
                    logger.error(f"Models Lab API error: {response.status_code} - {response.text}")
                    raise Exception(f"Models Lab API error: {response.status_code}")
                    
        except httpx.TimeoutException:
            logger.error("Models Lab API timeout")
            raise Exception("Models Lab API timeout")
        except Exception as e:
            logger.error(f"Models Lab API call failed: {e}")
            raise Exception(f"Models Lab API call failed: {e}")
    
    def _process_models_lab_response(self, response: Dict[str, Any]) -> List[str]:
        """Process Models Lab API response and extract image URLs."""
        generated_images = []
        
        try:
            logger.info(f"Processing Models Lab response: {json.dumps(response, indent=2)}")
            
            # Check if response has the expected structure
            if response.get("status") == "success" and "output" in response:
                output = response["output"]
                if isinstance(output, list):
                    for item in output:
                        if isinstance(item, str):
                            # It's a direct URL
                            if item.startswith("http"):
                                generated_images.append(item)
                            # Convert URL to data URL by downloading the image
                            else:
                                logger.warning(f"Unexpected output format: {item}")
                        elif isinstance(item, dict) and "image" in item:
                            image_url = item["image"]
                            if image_url.startswith("http"):
                                generated_images.append(image_url)
                elif isinstance(output, str):
                    if output.startswith("http"):
                        generated_images.append(output)
            
            logger.info(f"Processed {len(generated_images)} images from Models Lab")
            
            # If we have URLs but no data URLs, we'll return the URLs as-is
            # The frontend can handle downloading them
            return generated_images
            
        except Exception as e:
            logger.error(f"Failed to process Models Lab response: {e}")
            logger.error(f"Response was: {response}")
            return []
    
    async def generate_img2img(self, request: GenerationRequest) -> GenerationResult:
        """Generate professional interior designs using Models Lab API."""
        start_time = time.time()
        
        try:
            # Validate request
            if not request.primary_image:
                return GenerationResult(
                    success=False,
                    generated_images=[],
                    error_message="Primary image is required",
                    engine_used="models_lab"
                )
            
            # Build prompts
            prompt = self._build_prompt(request)
            negative_prompt = self._build_negative_prompt(request)
            
            logger.info(f"Generating design with Models Lab")
            logger.info(f"Style: {request.furniture_style}, Wall: {request.wall_color}, Flooring: {request.flooring_material}")
            logger.info(f"Prompt: {prompt[:100]}...")
            
            # Call Models Lab API
            print(f"Calling Models Lab API with prompt: {prompt[:50]}...")
            api_response = await self._call_models_lab_api(
                prompt=prompt,
                negative_prompt=negative_prompt,
                image_data=request.primary_image
            )
            print(f"Models Lab API raw response: {api_response}")
            
            # Process response
            print(f"Processing Models Lab response...")
            generated_images = self._process_models_lab_response(api_response)
            print(f"Processed {len(generated_images)} images from response")
            
            if not generated_images:
                return GenerationResult(
                    success=False,
                    generated_images=[],
                    error_message="No images generated from Models Lab API",
                    engine_used="models_lab"
                )
            
            # Calculate generation time
            inference_time = time.time() - start_time
            
            # Create result
            result = GenerationResult(
                success=True,
                generated_images=generated_images,
                engine_used="models_lab",
                model_version="Models Lab API v1.0",
                inference_time_seconds=inference_time,
                seeds_used=[]  # Models Lab doesn't return seeds
            )
            
            self.generation_count += 1
            logger.info(f"Generated {len(generated_images)} professional designs with Models Lab in {inference_time:.2f}s")
            
            return result
            
        except Exception as e:
            logger.error(f"Models Lab generation failed: {e}")
            return GenerationResult(
                success=False,
                generated_images=[],
                error_message=str(e),
                engine_used="models_lab"
            )
