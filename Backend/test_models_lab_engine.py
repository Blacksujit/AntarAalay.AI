#!/usr/bin/env python3
"""
Test Models Lab AI Engine - Professional Interior Design Generation
"""

import sys
import asyncio
from pathlib import Path

# Add backend directory to Python path
backend_dir = Path(__file__).parent
sys.path.insert(0, str(backend_dir))

async def test_models_lab_engine():
    try:
        print("🎨 Testing Models Lab AI Engine - Professional Interior Design")
        print("=" * 70)
        
        # Configuration with API key
        config = {
            'device': 'cpu',
            'models_lab_api_key': 'SysT5EwHzi8BgRIDn1eV3ZDuZelOSTFEccIYx2KYnMuoV5CGIRTUSbB4k13v'
        }
        
        # Create engine
        from app.services.ai_engine.models_lab_engine import ModelsLabEngine
        engine = ModelsLabEngine(config)
        print("✅ Models Lab engine created successfully")
        
        # Test health check
        print("🔍 Testing API connectivity...")
        health = await engine.health_check()
        print(f"Health check: {'✅ PASSED' if health else '❌ FAILED'}")
        
        # Test model info
        info = engine.get_model_info()
        print(f"Engine Type: {info['engine_type']}")
        print(f"Device: {info['device']}")
        print(f"Resolution: {info['resolution']}")
        print(f"Status: {info['status']}")
        print(f"API Provider: {info['api_provider']}")
        
        print(f"\n🎨 Supported Styles: {', '.join(info['supported_styles'])}")
        print(f"🏠 Supported Flooring: {', '.join(info['supported_flooring'])}")
        
        if not health:
            print("\n⚠️  API health check failed, but continuing with test...")
        
        # Test actual generation
        print("\n🎨 Testing Professional AI Design Generation...")
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
        
        # Generate designs
        print("🚀 Calling Models Lab API for professional designs...")
        result = await engine.generate_img2img(request)
        
        if result.success:
            print(f"✅ Professional design generation SUCCESS!")
            print(f"   Generated {len(result.generated_images)} professional designs")
            print(f"   Time: {result.inference_time_seconds:.2f}s")
            print(f"   Engine: {result.engine_used}")
            print(f"   Model: {result.model_version}")
            
            # Check if images are real data URLs
            for i, img_url in enumerate(result.generated_images):
                if img_url.startswith('data:image'):
                    print(f"   Design {i+1}: ✅ Professional design data ({len(img_url)} chars)")
                elif img_url.startswith('http'):
                    print(f"   Design {i+1}: ✅ Professional design URL: {img_url[:50]}...")
                else:
                    print(f"   Design {i+1}: ⚠️  Unexpected format: {img_url[:50]}...")
            
            return True
        else:
            print(f"❌ Professional design generation FAILED: {result.error_message}")
            return False
            
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = asyncio.run(test_models_lab_engine())
    print(f"\n{'🎉 MODELS LAB PROFESSIONAL DESIGN GENERATION WORKING!' if success else '❌ MODELS LAB INTEGRATION FAILED'}")
    if success:
        print("🚀 READY FOR PRODUCTION - PROFESSIONAL AI INTERIOR DESIGNS!")
