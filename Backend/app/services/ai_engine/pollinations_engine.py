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
from app.services.ai_engine.intent_prompt_builder import IntentBasedPromptBuilder

class PollinationsEngine(BaseEngine):
    """
    FREE Pollinations AI engine for interior design generation.
    No API key required - completely free!
    """
    
    def __init__(self, config: dict):
        self.generation_count = 0
        self.max_generations = 1000  # Very high limit for free service
        self.prompt_builder = IntentBasedPromptBuilder()
        print(f"PollinationsEngine initialized - FREE AI generation ready!")
    
    def _build_prompt(self, request: GenerationRequest, variation: int = 1) -> str:
        """Build comprehensive interior design prompt using intent-based Vastu approach."""
        return self.prompt_builder.build_intent_prompt(request, variation)
    
    def _build_negative_prompt(self, request: GenerationRequest) -> str:
        """Build negative prompt using intent-based approach."""
        return self.prompt_builder.build_negative_prompt(request)
    
    async def generate_img2img(self, request: GenerationRequest) -> GenerationResult:
        """Generate interior designs using FREE Pollinations AI."""
        start_time = time.time()
        
        try:
            # Build negative prompt once (same for all variations)
            negative_prompt = self._build_negative_prompt(request)
            
            print(f"Generating with Pollinations AI using Vastu principles - FREE!")
            print(f"Style: {request.furniture_style}")
            
            # Generate 3 Vastu-aligned variations with different prompts
            generated_images = []
            
            for i in range(3):
                variation = i + 1
                print(f"  Generating Vastu variation {variation}...")
                
                # Build variation-specific Vastu prompt
                variation_prompt = self._build_prompt(request, variation)
                print(f"    Vastu prompt {variation}: {variation_prompt[:80]}...")
                
                try:
                    # Pollinations AI endpoint - FREE, no API key!
                    seed = 42 + i  # Different seed for each variation
                    
                    # Clean prompt for URL - remove special characters
                    clean_prompt = variation_prompt.replace(',', ', ').replace('  ', ' ').strip()
                    
                    # Simple Pollinations AI URL
                    image_url = f"https://image.pollinations.ai/prompt/{clean_prompt}?width=512&height=512&seed={seed}&nologo=true"
                    
                    print(f"  Vastu variation {variation}: Generating...")
                    
                    # Download the generated image
                    async with httpx.AsyncClient(timeout=30) as client:
                        response = await client.get(image_url)
                        if response.status_code == 200:
                            # Convert to base64
                            image_data = response.content
                            base64_image = base64.b64encode(image_data).decode('utf-8')
                            data_url = f"data:image/jpeg;base64,{base64_image}"
                            generated_images.append(data_url)
                            print(f"  ✓ Vastu variation {variation} generated!")
                        else:
                            print(f"  ✗ Vastu variation {variation} failed: HTTP {response.status_code}")
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
