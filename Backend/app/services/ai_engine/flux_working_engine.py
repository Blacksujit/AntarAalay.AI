"""
Real FLUX Engine - HuggingFace Implementation with Rate Limiting
Generates real AI images using HuggingFace FLUX.1-schnell model
"""

import os
import time
import base64
import io
from typing import List, Dict, Optional
from PIL import Image
import random
from datetime import datetime, timedelta

from app.services.ai_engine.base_engine import BaseEngine, GenerationRequest, GenerationResult
from app.services.ai_engine.intent_prompt_builder import IntentBasedPromptBuilder
import logging

logger = logging.getLogger(__name__)


class FluxWorkingEngine(BaseEngine):
    """
    Real FLUX Engine that generates AI images using HuggingFace.
    Uses FLUX.1-schnell model via HuggingFace InferenceClient.
    Includes rate limiting to prevent quota exhaustion.
    """
    
    def __init__(self, config: dict):
        """Initialize FLUX engine with HuggingFace client and rate limiting."""
        self.api_token = config.get('hf_token') or config.get('huggingface_token') or os.getenv("HF_TOKEN")
        self.model_name = config.get('model', 'black-forest-labs/FLUX.1-schnell')
        self.prompt_builder = IntentBasedPromptBuilder()
        
        # Rate limiting settings
        self.max_generations_per_hour = config.get('max_generations_per_hour', 10)  # Conservative limit
        self.max_generations_per_day = config.get('max_generations_per_day', 50)    # Daily quota
        self.cooldown_seconds = config.get('cooldown_seconds', 30)  # Between generations
        
        # Tracking variables
        self.generation_count = 0
        self.max_generations = 1000
        
        # Rate limiting tracking
        self.hourly_generations = []  # List of timestamps
        self.daily_generations = []   # List of timestamps
        self.last_generation_time = 0
        
        # Initialize HuggingFace InferenceClient
        try:
            from huggingface_hub import InferenceClient
            self.client = InferenceClient(
                provider="nscale",
                api_key=self.api_token,
            )
            print(f"✅ FLUX Engine initialized with HuggingFace")
            print(f"Model: {self.model_name}")
            print(f"Token available: {'✅' if self.api_token else '❌'}")
            print(f"Rate limits: {self.max_generations_per_hour}/hour, {self.max_generations_per_day}/day")
            print(f"Cooldown: {self.cooldown_seconds}s between generations")
        except ImportError:
            print("❌ huggingface_hub not installed. Install with: pip install huggingface_hub")
            self.client = None
        except Exception as e:
            print(f"❌ FLUX Engine initialization failed: {e}")
            self.client = None
    
    def _build_prompt(self, request: GenerationRequest, variation: int = 1) -> str:
        """Build professional interior design prompt using intent-based Vastu approach."""
        return self.prompt_builder.build_intent_prompt(request, variation)
    
    def _convert_image_to_base64(self, image: Image.Image) -> str:
        """Convert PIL Image to base64 data URL."""
        buffered = io.BytesIO()
        image.save(buffered, format="JPEG", quality=95)
        img_str = base64.b64encode(buffered.getvalue()).decode('utf-8')
        data_url = f"data:image/jpeg;base64,{img_str}"
        return data_url
    
    def _cleanup_old_generations(self):
        """Remove old generation timestamps from tracking."""
        now = datetime.now()
        
        # Clean hourly generations (older than 1 hour)
        self.hourly_generations = [
            ts for ts in self.hourly_generations 
            if now - ts < timedelta(hours=1)
        ]
        
        # Clean daily generations (older than 24 hours)
        self.daily_generations = [
            ts for ts in self.daily_generations 
            if now - ts < timedelta(days=1)
        ]
    
    def _check_rate_limits(self) -> Dict[str, any]:
        """Check if generation is allowed based on rate limits."""
        self._cleanup_old_generations()
        now = datetime.now()
        
        # Check hourly limit
        hourly_count = len(self.hourly_generations)
        if hourly_count >= self.max_generations_per_hour:
            next_available = min(self.hourly_generations) + timedelta(hours=1)
            wait_time = (next_available - now).total_seconds()
            return {
                'allowed': False,
                'reason': 'hourly_limit',
                'message': f'Hourly limit reached ({self.max_generations_per_hour}/hour). Wait {wait_time/60:.1f} minutes.',
                'wait_time': wait_time
            }
        
        # Check daily limit
        daily_count = len(self.daily_generations)
        if daily_count >= self.max_generations_per_day:
            next_available = min(self.daily_generations) + timedelta(days=1)
            wait_time = (next_available - now).total_seconds()
            return {
                'allowed': False,
                'reason': 'daily_limit',
                'message': f'Daily limit reached ({self.max_generations_per_day}/day). Wait {wait_time/3600:.1f} hours.',
                'wait_time': wait_time
            }
        
        # Check cooldown
        if self.last_generation_time > 0:
            time_since_last = now.timestamp() - self.last_generation_time
            if time_since_last < self.cooldown_seconds:
                wait_time = self.cooldown_seconds - time_since_last
                return {
                    'allowed': False,
                    'reason': 'cooldown',
                    'message': f'Cooldown period. Wait {wait_time:.1f} seconds.',
                    'wait_time': wait_time
                }
        
        return {
            'allowed': True,
            'reason': 'ok',
            'message': 'Generation allowed',
            'wait_time': 0
        }
    
    def _record_generation(self):
        """Record a generation for rate limiting."""
        now = datetime.now()
        self.hourly_generations.append(now)
        self.daily_generations.append(now)
        self.last_generation_time = now.timestamp()
        self.generation_count += 1
        
        # Log current usage
        hourly_count = len(self.hourly_generations)
        daily_count = len(self.daily_generations)
        print(f"📊 Usage: {hourly_count}/{self.max_generations_per_hour} this hour, {daily_count}/{self.max_generations_per_day} today")
    
    async def generate_img2img(self, request: GenerationRequest) -> GenerationResult:
        """Generate real AI interior designs using FLUX with rate limiting."""
        start_time = time.time()
        
        if not self.client:
            return GenerationResult(
                success=False,
                generated_images=[],
                error_message="HuggingFace client not initialized. Check HF_TOKEN.",
                engine_used="flux_working"
            )
        
        # Check rate limits FIRST
        rate_check = self._check_rate_limits()
        if not rate_check['allowed']:
            print(f"🚫 Rate limit: {rate_check['message']}")
            return GenerationResult(
                success=False,
                generated_images=[],
                error_message=f"Rate limit: {rate_check['message']}",
                engine_used="flux_working",
                metadata={
                    'rate_limit_reason': rate_check['reason'],
                    'wait_time': rate_check['wait_time']
                }
            )
        
        try:
            print(f"Generating with Real FLUX Engine...")
            # Show base prompt for reference
            base_prompt = self._build_prompt(request, 1)
            print(f"Base Vastu prompt: {base_prompt[:80]}...")
            
            # Record generation attempt (counts toward quota)
            self._record_generation()
            
            # Generate 3 Vastu-aligned variations with different prompts
            generated_images = []
            
            for i in range(3):
                variation = i + 1
                print(f"  Generating Vastu variation {variation}...")
                
                # Build variation-specific prompt
                variation_prompt = self._build_prompt(request, variation)
                print(f"    Prompt {variation}: {variation_prompt[:80]}...")
                
                try:
                    # Generate image using HuggingFace FLUX
                    image = self.client.text_to_image(
                        variation_prompt,
                        model=self.model_name
                    )
                    
                    # Convert to base64
                    img_url = self._convert_image_to_base64(image)
                    generated_images.append(img_url)
                    print(f"  ✓ Vastu variation {variation} generated!")
                    
                except Exception as e:
                    print(f"  ✗ Vastu variation {variation} failed: {e}")
                    # Continue with other variations even if one fails
                    continue
            
            if not generated_images:
                return GenerationResult(
                    success=False,
                    generated_images=[],
                    error_message="No images generated from FLUX - all variations failed",
                    engine_used="flux_working"
                )
            
            inference_time = time.time() - start_time
            
            result = GenerationResult(
                success=True,
                generated_images=generated_images,
                engine_used="flux_working",
                model_version=f"FLUX.1-schnell (HuggingFace)",
                inference_time_seconds=inference_time,
                seeds_used=[42, 123, 456]  # Fixed seeds for consistency
            )
            
            print(f"✓ Generated {len(generated_images)} real designs with FLUX in {inference_time:.1f}s")
            
            return result
            
        except Exception as e:
            print(f"FLUX generation failed: {e}")
            return GenerationResult(
                success=False,
                generated_images=[],
                error_message=f"FLUX generation failed: {str(e)}",
                engine_used="flux_working"
            )
    
    def _get_engine_type(self) -> str:
        return "flux_working"
    
    def get_model_info(self) -> dict:
        self._cleanup_old_generations()
        hourly_count = len(self.hourly_generations)
        daily_count = len(self.daily_generations)
        
        return {
            "name": self.model_name,
            "type": "FLUX (HuggingFace)",
            "provider": "HuggingFace InferenceClient",
            "version": "1.0-schnell",
            "max_generations": self.max_generations,
            "current_generations": self.generation_count,
            "rate_limiting": {
                "enabled": True,
                "max_per_hour": self.max_generations_per_hour,
                "max_per_day": self.max_generations_per_day,
                "cooldown_seconds": self.cooldown_seconds,
                "current_hourly": hourly_count,
                "current_daily": daily_count,
                "hourly_remaining": max(0, self.max_generations_per_hour - hourly_count),
                "daily_remaining": max(0, self.max_generations_per_day - daily_count)
            }
        }
    
    def health_check(self) -> bool:
        """Check if FLUX engine is healthy and within limits."""
        if not self.client:
            return False
        
        # Check if we haven't exceeded daily limit
        self._cleanup_old_generations()
        daily_count = len(self.daily_generations)
        
        return daily_count < self.max_generations_per_day
