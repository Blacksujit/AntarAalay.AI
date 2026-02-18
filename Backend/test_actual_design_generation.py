#!/usr/bin/env python3
"""
Test the actual design generation API call
"""

import sys
from pathlib import Path

# Add backend directory to Python path
backend_dir = Path(__file__).parent
sys.path.insert(0, str(backend_dir))

import asyncio
import sqlite3

async def test_design_generation():
    """Test the actual design generation flow"""
    try:
        print("🎨 Testing Actual Design Generation Flow")
        print("=" * 50)
        
        # 1. Check if we have rooms to test with
        print("1. Checking for available rooms...")
        conn = sqlite3.connect('antaralay.db')
        cursor = conn.cursor()
        cursor.execute('SELECT id, user_id FROM rooms ORDER BY created_at DESC LIMIT 1')
        room = cursor.fetchone()
        conn.close()
        
        if not room:
            print("❌ No rooms found. Upload room images first.")
            return False
            
        room_id = room[0].split('_')[0]  # Get base room ID
        print(f"✅ Found room: {room_id}")
        
        # 2. Test the design generation directly
        print("2. Testing design generation...")
        from app.services.ai_engine import EngineFactory, EngineType
        from app.services.ai_engine.base_engine import GenerationRequest
        
        # Create engine
        engine = EngineFactory.create_engine(EngineType.LOCAL_SDXL, {'device': 'cpu'})
        print("✅ Engine created")
        
        # Create test image
        from PIL import Image
        import io
        
        test_image = Image.new('RGB', (512, 512), color='lightblue')
        buffer = io.BytesIO()
        test_image.save(buffer, format='JPEG')
        image_bytes = buffer.getvalue()
        
        # Create room images dict
        room_images = {
            "north": image_bytes,
            "south": image_bytes,
            "east": image_bytes,
            "west": image_bytes
        }
        
        # Create generation request
        request = GenerationRequest(
            primary_image=image_bytes,
            room_images=room_images,
            room_type="living",
            furniture_style="modern",
            wall_color="white",
            flooring_material="hardwood"
        )
        print("✅ Generation request created")
        
        # Generate images
        result = await engine.generate_img2img(request)
        print("✅ Generation completed")
        
        if result.success:
            print(f"✅ Generation SUCCESS!")
            print(f"   Generated {len(result.generated_images)} images")
            print(f"   Time: {result.inference_time_seconds:.2f}s")
            
            # Check if images are real data URLs
            for i, img in enumerate(result.generated_images):
                if img.startswith('data:image/jpeg;base64,') and len(img) > 1000:
                    print(f"   Image {i+1}: ✅ REAL JPEG data ({len(img)} chars)")
                else:
                    print(f"   Image {i+1}: ❌ Invalid format")
            
            return True
        else:
            print(f"❌ Generation FAILED: {result.error_message}")
            return False
            
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = asyncio.run(test_design_generation())
    print(f"\n{'🎉 DESIGN GENERATION WORKING!' if success else '❌ DESIGN GENERATION BROKEN'}")
    if success:
        print("💡 The issue is likely in the frontend API call")
        print("💡 Check browser network tab for design generation requests")
