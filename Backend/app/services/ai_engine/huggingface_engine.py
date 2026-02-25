"""
Hugging Face Inference Engine - Updated for new API
Uses InferenceClient with nscale provider for FLUX.1-schnell
"""

import os
import time
import base64
import io
from typing import List, Optional
from PIL import Image

from app.services.ai_engine.base_engine import BaseEngine, GenerationRequest, GenerationResult
from app.services.ai_engine.intent_prompt_builder import IntentBasedPromptBuilder
import logging

logger = logging.getLogger(__name__)


class HuggingFaceEngine(BaseEngine):
    """
    Hugging Face Inference Engine using new InferenceClient API.
    Supports FLUX.1-schnell and other models via nscale provider.
    """
    
    def __init__(self, config: dict):
        """Initialize Hugging Face engine."""
        self.api_token = config.get('hf_token') or os.getenv("HF_TOKEN")
        self.model_name = config.get('model', 'black-forest-labs/FLUX.1-schnell')
        self.prompt_builder = IntentBasedPromptBuilder()
        self.generation_count = 0
        self.max_generations = 1000
        
        print(f"HuggingFaceEngine initialized with token: {bool(self.api_token)}")
        print(f"Model: {self.model_name}")
        
        # Initialize InferenceClient
        try:
            from huggingface_hub import InferenceClient
            self.client = InferenceClient(
                model=self.model_name,
                token=self.api_token,
                provider="nscale"
            )
            print(f"InferenceClient created successfully with nscale provider")
        except Exception as e:
            print(f"Failed to create InferenceClient: {e}")
            self.client = None
    
    def _build_prompt(self, request: GenerationRequest, variation: int = 1) -> str:
        """Build interior design prompt using intent-based Vastu approach."""
        return self.prompt_builder.build_intent_prompt(request, variation)
    
    async def generate_img2img(self, request: GenerationRequest) -> GenerationResult:
        """Generate interior designs using Hugging Face FLUX API."""
        start_time = time.time()
        
        try:
            if not self.client:
                return GenerationResult(
                    success=False,
                    generated_images=[],
                    error_message="InferenceClient not initialized",
                    engine_used="huggingface"
                )
            
            # Build Vastu prompts and generate variations
            print(f"Generating with FLUX.1-schnell using Vastu principles...")
            generated_images = []
            
            for i in range(3):
                variation = i + 1
                print(f"  Generating Vastu variation {variation}...")
                
                # Build variation-specific Vastu prompt
                variation_prompt = self._build_prompt(request, variation)
                print(f"    Vastu prompt {variation}: {variation_prompt[:80]}...")
                
                try:
                    # Use text_to_image for FLUX.1-schnell (synchronous call)
                    image = self.client.text_to_image(
                        variation_prompt,
                        model=self.model_name,
                        seed=42 + i,
                        width=1024,
                        height=1024,
                        num_inference_steps=4,
                        guidance_scale=3.5,
                    )
                    
                    # Convert PIL Image to base64
                    buffered = io.BytesIO()
                    image.save(buffered, format="JPEG", quality=95)
                    img_str = base64.b64encode(buffered.getvalue()).decode('utf-8')
                    data_url = f"data:image/jpeg;base64,{img_str}"
                    generated_images.append(data_url)
                    print(f"  ✓ Vastu variation {variation} generated!")
                    
                except Exception as e:
                    print(f"  ✗ Vastu variation {variation} failed: {e}")
                    continue
            
            if not generated_images:
                return GenerationResult(
                    success=False,
                    generated_images=[],
                    error_message="No images generated from Hugging Face API",
                    engine_used="huggingface"
                )
            
            inference_time = time.time() - start_time
            
            result = GenerationResult(
                success=True,
                generated_images=generated_images,
                engine_used="huggingface",
                model_version="FLUX.1-schnell",
                inference_time_seconds=inference_time,
                seeds_used=[42, 43, 44]
            )
            
            self.generation_count += 1
            print(f"✓ Generated {len(generated_images)} designs with FLUX.1-schnell in {inference_time:.1f}s")
            
            return result
            
        except Exception as e:
            print(f"Hugging Face generation failed: {e}")
            return GenerationResult(
                success=False,
                generated_images=[],
                error_message=f"Hugging Face generation failed: {str(e)}",
                engine_used="huggingface"
            )
    
    def _get_engine_type(self) -> str:
        return "huggingface"
    
    def get_model_info(self) -> dict:
        return {
            "name": self.model_name,
            "type": "FLUX",
            "provider": "Hugging Face (nscale)",
            "version": "1.0-schnell",
            "max_generations": self.max_generations,
            "current_generations": self.generation_count
        }
    
    def health_check(self) -> bool:
        return self.generation_count < self.max_generations and bool(self.api_token) and bool(self.client)

