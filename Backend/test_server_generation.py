#!/usr/bin/env python3
"""
Test server generation with fixed factory
"""

import sys
import asyncio
from pathlib import Path

# Add backend directory to Python path
backend_dir = Path(__file__).parent
sys.path.insert(0, str(backend_dir))

from app.services.ai_engine import EngineFactory, EngineType
from app.services.ai_engine.base_engine import GenerationRequest

async def test_server_generation():
    print("🎨 Testing Server Generation with Fixed Factory")
    print("=" * 55)
    
    # Create engine (same as server will use)
    engine = EngineFactory.create_engine(EngineType.LOCAL_SDXL, {'device': 'cpu'})
    
    info = engine.get_model_info()
    print(f"✅ Server will use: {info['engine_type']}")
    print(f"✅ Status: {info['status']}")
    
    # Test health
    health = await engine.health_check()
    print(f"✅ Health check: {'PASSED' if health else 'FAILED'}")
    
    # Test actual generation (same as API call)
    from PIL import Image
    import io
    
    test_image = Image.new('RGB', (512, 512), color='lightblue')
    buffer = io.BytesIO()
    test_image.save(buffer, format='JPEG')
    image_bytes = buffer.getvalue()
    
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
    
    # Generate (this is what the API does)
    result = await engine.generate_img2img(request)
    
    if result.success:
        print(f"✅ Generation SUCCESS!")
        print(f"   Generated {len(result.generated_images)} images")
        print(f"   Time: {result.inference_time_seconds:.2f}s")
        print(f"   Engine: {result.engine_used}")
        
        # Verify real images
        for i, img in enumerate(result.generated_images):
            if img.startswith('data:image/jpeg;base64,') and len(img) > 1000:
                print(f"   Image {i+1}: ✅ REAL JPEG data ({len(img)} chars)")
            else:
                print(f"   Image {i+1}: ❌ Invalid")
        
        return True
    else:
        print(f"❌ Generation FAILED: {result.error_message}")
        return False

if __name__ == "__main__":
    success = asyncio.run(test_server_generation())
    print(f"\n{'🚀 SERVER READY FOR PRODUCTION!' if success else '❌ SERVER NOT READY'}")
