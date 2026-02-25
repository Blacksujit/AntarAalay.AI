"""
Pollinations AI Engine - FREE Image Generation
Uses Pollinations.ai free Stable Diffusion API (no API key required)
"""

import httpx
import time
import uuid
import base64
import io
from typing import List, Optional
from PIL import Image

from app.services.ai_engine.base_engine import BaseEngine, GenerationRequest, GenerationResult


class PollinationsEngine(BaseEngine):
    """
    FREE Pollinations AI engine for interior design generation.
    No API key required - completely free!
    """
    
    def __init__(self, config: dict):
        self.generation_count = 0
        self.max_generations = 1000  # Very high limit for free service
        print(f"PollinationsEngine initialized - FREE AI generation ready!")
    
    def _build_prompt(self, request: GenerationRequest) -> str:
        """Build comprehensive interior design prompt."""
        style_descriptors = {
            'modern': 'contemporary minimalist interior design, clean lines, neutral colors',
            'traditional': 'classic interior design, warm traditional furniture, elegant details',
            'minimalist': 'minimalist interior, simple clean design, neutral palette',
            'industrial': 'industrial loft design, raw materials, urban aesthetic'
        }
        
        style_desc = style_descriptors.get(request.furniture_style, request.furniture_style)
        
        # Create clean prompt without newlines
        room_type = request.room_type if request.room_type else 'room'
        wall_color = request.wall_color if request.wall_color else 'white'
        flooring = request.flooring_material if request.flooring_material else 'hardwood'
        
        prompt = f"Professional interior design photograph, {style_desc}, {room_type} with {wall_color} walls, {flooring} flooring, high quality furniture arrangement, natural lighting, architectural photography, 4k, detailed, realistic"
        
        return prompt
    
    def _build_negative_prompt(self, request: GenerationRequest) -> str:
        """Build negative prompt."""
        return "cartoon, anime, 3d render, illustration, painting, text, watermark, blurry, low quality, distorted"
    
    async def generate_img2img(self, request: GenerationRequest) -> GenerationResult:
        """Generate interior designs using FREE Pollinations AI."""
        start_time = time.time()
        
        try:
            # Build prompt
            prompt = self._build_prompt(request)
            negative_prompt = self._build_negative_prompt(request)
            
            print(f"Generating with Pollinations AI - FREE!")
            print(f"Style: {request.furniture_style}")
            print(f"Prompt: {prompt[:80]}...")
            
            # Generate 3 variations with different seeds
            generated_images = []
            
            for i in range(3):
                try:
                    # Pollinations AI endpoint - FREE, no API key!
                    seed = 42 + i  # Different seed for each variation
                    
                    # Clean prompt for URL - remove special characters
                    clean_prompt = prompt.replace(',', ', ').replace('  ', ' ').strip()
                    
                    # Simple Pollinations AI URL
                    image_url = f"https://image.pollinations.ai/prompt/{clean_prompt}?width=512&height=512&seed={seed}&nologo=true"
                    
                    print(f"  Variation {i+1}: Generating...")
                    
                    # Download the generated image
                    async with httpx.AsyncClient(timeout=30) as client:
                        response = await client.get(image_url)
                        if response.status_code == 200:
                            # Convert to base64
                            image_data = response.content
                            base64_image = base64.b64encode(image_data).decode('utf-8')
                            data_url = f"data:image/jpeg;base64,{base64_image}"
                            generated_images.append(data_url)
                            print(f"  ✓ Variation {i+1} generated!")
                        else:
                            print(f"  ✗ Variation {i+1} failed: HTTP {response.status_code}")
                            continue
                        
                except Exception as e:
                    print(f"  ✗ Variation {i+1} failed: {e}")
                    continue
            
            if not generated_images:
                return GenerationResult(
                    success=False,
                    generated_images=[],
                    error_message="Pollinations AI generation failed",
                    engine_used="pollinations"
                )
            
            inference_time = time.time() - start_time
            
            result = GenerationResult(
                success=True,
                generated_images=generated_images,
                engine_used="pollinations",
                model_version="Pollinations AI Stable Diffusion",
                inference_time_seconds=inference_time,
                seeds_used=[42, 43, 44]
            )
            
            self.generation_count += 1
            print(f"✓ Generated {len(generated_images)} designs with Pollinations AI in {inference_time:.1f}s")
            
            return result
            
        except Exception as e:
            print(f"Pollinations AI failed: {e}")
            return GenerationResult(
                success=False,
                generated_images=[],
                error_message=f"Pollinations AI failed: {str(e)}",
                engine_used="pollinations"
            )
    
    def _get_engine_type(self) -> str:
        return "pollinations"
    
    def get_model_info(self) -> dict:
        return {
            "name": "Pollinations AI",
            "type": "Stable Diffusion",
            "provider": "Pollinations.ai",
            "price": "FREE",
            "max_generations": self.max_generations,
            "current_generations": self.generation_count
        }
    
    def health_check(self) -> bool:
        return True  # Always healthy - no auth needed
