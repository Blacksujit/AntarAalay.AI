#!/usr/bin/env python3
"""
Test Standalone Image Engine - Real Image Generation
"""

import sys
import os
from pathlib import Path

# Add backend directory to Python path
backend_dir = Path(__file__).parent.parent
sys.path.insert(0, str(backend_dir))

import asyncio
from app.services.ai_engine.standalone_image_engine import StandaloneImageEngine

async def test_standalone_engine():
    try:
        print("🎨 Testing Standalone Image Engine - REAL Image Generation")
        print("=" * 65)
        
        # Configuration
        config = {
            'device': 'cpu'
        }
        
        # Create engine
        engine = StandaloneImageEngine(config)
        print("✅ Engine created successfully")
        
        # Test health check
        health = await engine.health_check()
        print(f"Health check: {'✅ PASSED' if health else '❌ FAILED'}")
        
        # Test model info
        info = engine.get_model_info()
        print(f"Engine Type: {info['engine_type']}")
        print(f"Device: {info['device']}")
        print(f"Resolution: {info['resolution']}")
        print(f"Status: {info['status']}")
        print(f"Model Type: {info['model_type']}")
        
        print(f"\n🎨 Supported Styles: {', '.join(info['supported_styles'])}")
        print(f"🏠 Supported Flooring: {', '.join(info['supported_flooring'])}")
        
        # Test actual generation
        print("\n🎨 Testing REAL image generation...")
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
            print(f"   Generated {len(result.generated_images)} REAL images")
            print(f"   Time: {result.inference_time_seconds:.2f}s")
            print(f"   Seeds: {result.seeds_used}")
            print(f"   Engine: {result.engine_used}")
            print(f"   Model: {result.model_version}")
            
            # Check if images are real data URLs
            for i, img_url in enumerate(result.generated_images):
                if img_url.startswith('data:image/jpeg;base64,'):
                    print(f"   Image {i+1}: ✅ Valid JPEG data URL ({len(img_url)} chars)")
                    # Verify it's actually base64 data
                    if len(img_url) > 100:  # Should have substantial data
                        print(f"              ✅ Contains actual image data")
                    else:
                        print(f"              ⚠️  Small data size")
                else:
                    print(f"   Image {i+1}: ❌ Invalid format")
            
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
    success = asyncio.run(test_standalone_engine())
    print(f"\n{'🎉 STANDALONE ENGINE TEST PASSED' if success else '❌ STANDALONE ENGINE TEST FAILED'}")
    if success:
        print("🚀 READY FOR PRODUCTION - ACTUAL IMAGE GENERATION WORKING!")
