"""
Working FLUX Engine - Simple Implementation
Generates mock images for testing without requiring API tokens
"""

import time
import base64
import io
from typing import List
from PIL import Image, ImageDraw
import random

from app.services.ai_engine.base_engine import BaseEngine, GenerationRequest, GenerationResult
import logging

logger = logging.getLogger(__name__)


class FluxWorkingEngine(BaseEngine):
    """
    Working FLUX Engine that generates mock images for testing.
    Creates simple colored blocks with text to simulate generated designs.
    """
    
    def __init__(self, config: dict):
        """Initialize FLUX working engine."""
        self.api_token = config.get('huggingface_token')
        self.model_name = config.get('model', 'black-forest-labs/FLUX.1-schnell')
        self.generation_count = 0
        self.max_generations = 1000
        
        print(f"FluxWorkingEngine initialized (mock mode)")
        print(f"Model: {self.model_name}")
    
    def _create_mock_image(self, text: str, color: tuple, seed: int) -> str:
        """Create a simple mock image with colored background and text."""
        # Create image
        img = Image.new('RGB', (512, 512), color)
        draw = ImageDraw.Draw(img)
        
        # Add text
        try:
            # Try to use a basic font
            draw.text((50, 200), f"FLUX Mock", fill='white')
            draw.text((50, 250), f"Variation {seed}", fill='white')
            draw.text((50, 300), f"{text}", fill='white')
        except:
            # Fallback if font not available
            pass
        
        # Convert to base64
        buffered = io.BytesIO()
        img.save(buffered, format="JPEG", quality=95)
        img_str = base64.b64encode(buffered.getvalue()).decode('utf-8')
        data_url = f"data:image/jpeg;base64,{img_str}"
        
        return data_url
    
    def _build_prompt(self, request: GenerationRequest) -> str:
        """Build interior design prompt for FLUX."""
        style_desc = request.furniture_style or 'modern'
        room_type = request.room_type or 'living room'
        wall_color = request.wall_color or 'white'
        flooring = request.flooring_material or 'hardwood'
        
        return f"{style_desc} {room_type} with {wall_color} walls and {flooring} flooring"
    
    async def generate_img2img(self, request: GenerationRequest) -> GenerationResult:
        """Generate mock interior designs using simple colored images."""
        start_time = time.time()
        
        try:
            print(f"Generating with FLUX Working Engine (mock mode)...")
            prompt = self._build_prompt(request)
            print(f"Prompt: {prompt[:80]}...")
            
            # Generate 3 mock variations with different colors
            generated_images = []
            colors = [
                (135, 206, 235),  # Sky blue
                (144, 238, 144),  # Light green
                (255, 182, 193),  # Light pink
            ]
            
            for i in range(3):
                seed = 42 + i
                color = colors[i % len(colors)]
                
                print(f"  Generating variation {i+1} with seed {seed}...")
                
                # Create mock image
                img_url = self._create_mock_image(
                    f"{prompt} #{i+1}",
                    color,
                    seed
                )
                generated_images.append(img_url)
                print(f"  ✓ Variation {i+1} generated!")
            
            if not generated_images:
                return GenerationResult(
                    success=False,
                    generated_images=[],
                    error_message="No images generated from FLUX Working Engine",
                    engine_used="flux_working"
                )
            
            inference_time = time.time() - start_time
            
            result = GenerationResult(
                success=True,
                generated_images=generated_images,
                engine_used="flux_working",
                model_version="FLUX.1-schnell (mock)",
                inference_time_seconds=inference_time,
                seeds_used=[42, 43, 44]
            )
            
            self.generation_count += 1
            print(f"✓ Generated {len(generated_images)} mock designs with FLUX Working Engine in {inference_time:.1f}s")
            
            return result
            
        except Exception as e:
            print(f"FLUX Working Engine generation failed: {e}")
            return GenerationResult(
                success=False,
                generated_images=[],
                error_message=f"FLUX Working Engine generation failed: {str(e)}",
                engine_used="flux_working"
            )
    
    def _get_engine_type(self) -> str:
        return "flux_working"
    
    def get_model_info(self) -> dict:
        return {
            "name": self.model_name,
            "type": "FLUX (mock)",
            "provider": "Working Engine (no API required)",
            "version": "1.0-schnell (mock)",
            "max_generations": self.max_generations,
            "current_generations": self.generation_count
        }
    
    def health_check(self) -> bool:
        return self.generation_count < self.max_generations
