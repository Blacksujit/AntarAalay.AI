#!/usr/bin/env python3
"""
Direct Models Lab API test
"""

import sys
import asyncio
import httpx
import json
import base64
from io import BytesIO
from pathlib import Path
from PIL import Image

# Add backend directory to Python path
backend_dir = Path(__file__).parent
sys.path.insert(0, str(backend_dir))

async def test_models_lab_direct():
    try:
        print("🔍 Direct Models Lab API Test")
        print("=" * 40)
        
        # API configuration
        api_key = "SysT5EwHzi8BgRIDn1eV3ZDuZelOSTFEccIYx2KYnMuoV5CGIRTUSbB4k13v"
        base_url = "https://modelslab.com/api/v1"
        
        # Create test image
        test_image = Image.new('RGB', (512, 512), color='lightblue')
        buffer = BytesIO()
        test_image.save(buffer, format='JPEG')
        image_bytes = buffer.getvalue()
        base64_image = base64.b64encode(image_bytes).decode('utf-8')
        
        # Test different endpoints
        endpoints_to_test = [
            "/image_gen",
            "/txt2img", 
            "/img2img",
            "/stable-diffusion",
            "/v1/stable-diffusion",
            "/v1/image-gen"
        ]
        
        for endpoint in endpoints_to_test:
            print(f"\n🧪 Testing endpoint: {endpoint}")
            
            payload = {
                "key": api_key,
                "prompt": "modern interior design, professional photography, high quality",
                "negative_prompt": "blurry, low quality, distorted",
                "init_image": base64_image,
                "width": 512,
                "height": 512,
                "samples": 1,
                "num_inference_steps": 20,
                "guidance_scale": 7.5,
                "strength": 0.7
            }
            
            try:
                async with httpx.AsyncClient(timeout=30.0) as client:
                    response = await client.post(
                        f"{base_url}{endpoint}",
                        json=payload,
                        headers={"Content-Type": "application/json"}
                    )
                    
                    print(f"   Status: {response.status_code}")
                    
                    if response.status_code == 200:
                        result = response.json()
                        print(f"   ✅ Response: {json.dumps(result, indent=2)[:300]}...")
                        if result.get("status") == "success":
                            return True
                    else:
                        print(f"   ❌ FAILED: {response.text}")
                        
            except Exception as e:
                print(f"   ❌ ERROR: {e}")
        
        # Test if we can at least access the API
        print(f"\n🔍 Testing basic API access...")
        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                response = await client.get(
                    f"{base_url}/models",
                    headers={"Authorization": f"Bearer {api_key}"}
                )
                print(f"Models endpoint status: {response.status_code}")
                if response.status_code == 200:
                    print(f"Response: {response.text[:200]}...")
        except Exception as e:
            print(f"Basic access failed: {e}")
        
        return False
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = asyncio.run(test_models_lab_direct())
    print(f"\n{'🎉 MODELS LAB API WORKING!' if success else '❌ MODELS LAB API NOT WORKING'}")
