#!/usr/bin/env python3
"""
Test Working SD15 Engine - Actual Image Generation
"""

import sys
import os
from pathlib import Path

# Add backend directory to Python path
backend_dir = Path(__file__).parent.parent
sys.path.insert(0, str(backend_dir))

import asyncio
from app.services.ai_engine.working_sd15_engine import WorkingSD15Engine

async def test_working_engine():
    try:
        print("🎨 Testing Working SD15 Engine - Actual Image Generation")
        print("=" * 65)
        
        # Configuration
        config = {
            'device': 'cpu',
            'num_inference_steps': 20,  # Reduced for CPU
            'guidance_scale': 7.5,
            'strength': 0.6
        }
        
        # Create engine
        engine = WorkingSD15Engine(config)
        print("✅ Engine created successfully")
        
        # Test health check
        health = await engine.health_check()
        print(f"Health check: {'✅ PASSED' if health else '❌ FAILED'}")
        
        # Test model info
        info = engine.get_model_info()
        print(f"Engine Type: {info['engine_type']}")
        print(f"Model: {info['model_id']}")
        print(f"Device: {info['device']}")
        print(f"Mock Mode: {info['mock_mode']}")
        print(f"Status: {info['status']}")
        
        # Test actual generation
        print("\n🎨 Testing image generation...")
        from app.services.ai_engine.base_engine import GenerationRequest
        
        # Create a test image
        from PIL import Image
        import io
        
        test_image = Image.new('RGB', (512, 512), color='lightblue')
        buffer = io.BytesIO()
        test_image.save(buffer, format='JPEG')
        image_bytes = buffer.getvalue()
        
        # Create generation request
        request = GenerationRequest(
            primary_image=image_bytes,
            room_images={
                "north": image_bytes,
                "south": image_bytes,
                "east": image_bytes,
                "west": image_bytes
            },
            room_type="living",
            furniture_style="modern",
            wall_color="white",
            flooring_material="hardwood"
        )
        
        # Generate images
        result = await engine.generate_img2img(request)
        
        if result.success:
            print(f"✅ Generation successful!")
            print(f"   Generated {len(result.generated_images)} images")
            print(f"   Time: {result.inference_time_seconds:.2f}s")
            print(f"   Seeds: {result.seeds_used}")
            print(f"   Engine: {result.engine_used}")
            
            # Check if images are real data URLs
            for i, img_url in enumerate(result.generated_images):
                if img_url.startswith('data:image'):
                    print(f"   Image {i+1}: Valid data URL ({len(img_url)} chars)")
                else:
                    print(f"   Image {i+1}: Invalid format")
            
            return True
        else:
            print(f"❌ Generation failed: {result.error_message}")
            return False
            
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = asyncio.run(test_working_engine())
    print(f"\n{'🎉 WORKING ENGINE TEST PASSED' if success else '❌ WORKING ENGINE TEST FAILED'}")
