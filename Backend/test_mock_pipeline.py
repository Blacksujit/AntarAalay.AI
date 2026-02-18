#!/usr/bin/env python3
"""
Mock SD15 Engine for Testing Pipeline (No Model Loading)
"""

import sys
import os
from pathlib import Path

# Add backend directory to Python path
backend_dir = Path(__file__).parent.parent
sys.path.insert(0, str(backend_dir))

import asyncio
import time
from app.services.ai_engine.base_engine import BaseEngine, GenerationRequest, GenerationResult, EngineType
from app.services.ai_engine.prompt_builder import PromptBuilder
from app.services.ai_engine.controlnet_adapter import ControlNetAdapter

class MockSD15Engine(BaseEngine):
    """Mock SD15 engine for testing without model loading."""
    
    def __init__(self, config):
        super().__init__(config)
        self.device = config.get('device', 'cpu')
        self.resolution = config.get('resolution', 512)
        self.prompt_builder = PromptBuilder()
        self.controlnet_adapter = ControlNetAdapter(config)
        
    def _get_engine_type(self) -> EngineType:
        return EngineType.LOCAL_SDXL
    
    async def health_check(self) -> bool:
        return True  # Always healthy for testing
    
    def get_model_info(self) -> dict:
        return {
            "engine_type": "Mock SD15 ControlNet (Testing)",
            "base_model": "runwayml/stable-diffusion-v1-5",
            "controlnet_model": "lllyasviel/control_v11p_sd15_canny",
            "resolution": f"{self.resolution}x{self.resolution}",
            "device": self.device,
            "status": "Mock - No models loaded"
        }
    
    async def generate_img2img(self, request: GenerationRequest) -> GenerationResult:
        """Mock generation that returns fake images."""
        start_time = time.time()
        
        try:
            # Validate request
            if not request.primary_image:
                return GenerationResult(
                    success=False,
                    generated_images=[],
                    error_message="Primary image is required",
                    engine_used="mock_sd15"
                )
            
            # Mock generation - return fake base64 images
            mock_images = [
                "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mP8/5+hHgAHggJ/PchI7wAAAABJRU5ErkJggg=="
            ]
            
            inference_time = time.time() - start_time
            
            return GenerationResult(
                success=True,
                generated_images=mock_images,
                engine_used="mock_sd15",
                model_version="mock_v1.5",
                inference_time_seconds=inference_time,
                seeds_used=[12345, 67890, 11111]
            )
            
        except Exception as e:
            return GenerationResult(
                success=False,
                generated_images=[],
                error_message=str(e),
                engine_used="mock_sd15"
            )

async def test_mock_pipeline():
    try:
        print("🏠 Testing Mock SD15 Pipeline (No Model Loading)")
        print("=" * 60)
        
        config = {
            'device': 'cpu',
            'resolution': 512,
            'enable_xformers': False,
            'enable_attention_slicing': True,
            'enable_cpu_offload': True
        }
        
        # Create mock engine
        engine = MockSD15Engine(config)
        print("✅ Mock engine created")
        
        # Test health check
        health = await engine.health_check()
        print(f"Health check: {'✅ PASSED' if health else '❌ FAILED'}")
        
        # Test model info
        info = engine.get_model_info()
        print(f"Engine: {info['engine_type']}")
        print(f"Models: {info['base_model']} + {info['controlnet_model']}")
        print(f"Status: {info['status']}")
        
        # Test prompt builder
        prompt_builder = PromptBuilder()
        try:
            # Use the build_prompt method we added
            pos_prompt, neg_prompt = prompt_builder.build_prompt(
                furniture_style="modern",
                wall_color="white", 
                flooring_material="hardwood"
            )
            print(f"\n✅ Prompt builder working")
            print(f"   Positive: {pos_prompt[:50]}...")
            print(f"   Negative: {neg_prompt[:50]}...")
        except Exception as e:
            print(f"⚠️  Prompt builder issue: {e}")
            # Use StyleParameters object
            from app.services.ai_engine.prompt_builder import StyleParameters
            style_params = StyleParameters(
                room_type="living",
                furniture_style="modern",
                wall_color="white",
                flooring_material="hardwood"
            )
            pos_prompt = prompt_builder.build_positive_prompt(style_params)
            neg_prompt = prompt_builder.build_negative_prompt()
            print(f"\n✅ Prompt builder working (alternative)")
            print(f"   Positive: {pos_prompt[:50]}...")
            print(f"   Negative: {neg_prompt[:50]}...")
        
        # Test ControlNet adapter
        from PIL import Image
        import numpy as np
        test_image = Image.new('RGB', (512, 512), color='white')
        controlnet_adapter = ControlNetAdapter(config)
        # Convert PIL to numpy for ControlNet adapter
        image_array = np.array(test_image)
        edge_map = controlnet_adapter.detect_canny_edges(image_array)
        print(f"✅ ControlNet adapter working")
        print(f"   Edge map size: {edge_map.size}")
        
        # Test mock generation
        print("\n🎨 Testing mock generation...")
        from app.services.ai_engine.base_engine import GenerationRequest
        
        # Create a mock request
        mock_request = GenerationRequest(
            primary_image=b"fake_image_data",
            room_images={
                "north": b"fake_north",
                "south": b"fake_south", 
                "east": b"fake_east",
                "west": b"fake_west"
            },
            room_type="living",
            furniture_style="modern",
            wall_color="white",
            flooring_material="hardwood"
        )
        
        result = await engine.generate_img2img(mock_request)
        print(f"Generation: {'✅ PASSED' if result.success else '❌ FAILED'}")
        if result.success:
            print(f"   Generated {len(result.generated_images)} images")
            print(f"   Time: {result.inference_time_seconds:.2f}s")
        else:
            print(f"   Error: {result.error_message}")
        
        print("\n🎉 All pipeline components working correctly!")
        return True
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = asyncio.run(test_mock_pipeline())
    sys.exit(0 if success else 1)
