#!/usr/bin/env python3
"""
Check Models Lab API documentation endpoints
"""

import sys
import asyncio
import httpx
import json
from pathlib import Path

# Add backend directory to Python path
backend_dir = Path(__file__).parent
sys.path.insert(0, str(backend_dir))

async def check_models_lab_endpoints():
    try:
        print("🔍 Checking Models Lab API Endpoints")
        print("=" * 45)
        
        api_key = "SysT5EwHzi8BgRIDn1eV3ZDuZelOSTFEccIYx2KYnMuoV5CGIRTUSbB4k13v"
        base_url = "https://modelslab.com"
        
        # Test different base URLs and endpoints
        test_configs = [
            ("https://modelslab.com/api/v6", "/text2img"),
            ("https://modelslab.com/api/v6", "/img2img"),
            ("https://modelslab.com/api/v4", "/dreambooth"),
            ("https://modelslab.com/api/v4", "/stable_diffusion"),
            ("https://api.modelslab.com", "/v1/text2img"),
            ("https://api.modelslab.com", "/v1/img2img"),
            ("https://modelslab.com/api/v3", "/text2img"),
            ("https://modelslab.com/api/v3", "/img2img"),
        ]
        
        for base, endpoint in test_configs:
            print(f"\n🧪 Testing: {base}{endpoint}")
            
            payload = {
                "key": api_key,
                "prompt": "modern interior design",
                "samples": 1,
                "width": 512,
                "height": 512
            }
            
            try:
                async with httpx.AsyncClient(timeout=15.0) as client:
                    response = await client.post(
                        f"{base}{endpoint}",
                        json=payload,
                        headers={"Content-Type": "application/json"}
                    )
                    
                    print(f"   Status: {response.status_code}")
                    
                    if response.status_code == 200:
                        result = response.json()
                        if result.get("status") == "success":
                            print(f"   🎉 FOUND WORKING ENDPOINT!")
                            print(f"   Response: {json.dumps(result, indent=2)[:300]}...")
                            return base, endpoint
                        else:
                            print(f"   Response: {result.get('message', 'Unknown error')}")
                    else:
                        print(f"   Error: {response.text[:100]}")
                        
            except Exception as e:
                print(f"   Exception: {e}")
        
        # Let's also try to access their main API docs
        print(f"\n📚 Checking API documentation...")
        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                response = await client.get("https://modelslab.com/docs")
                print(f"Docs page status: {response.status_code}")
        except Exception as e:
            print(f"Docs access failed: {e}")
        
        return None, None
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        return None, None

if __name__ == "__main__":
    base, endpoint = asyncio.run(check_models_lab_endpoints())
    if base and endpoint:
        print(f"\n🎉 FOUND WORKING ENDPOINT: {base}{endpoint}")
    else:
        print(f"\n❌ NO WORKING ENDPOINT FOUND")
