#!/usr/bin/env python3
"""
Check the actual server response for design generation
"""

import sys
from pathlib import Path

# Add backend directory to Python path
backend_dir = Path(__file__).parent
sys.path.insert(0, str(backend_dir))

import requests
import json

def test_design_generation_api():
    """Test the actual API endpoint that was called"""
    
    print("🔍 Checking Design Generation API Response")
    print("=" * 50)
    
    # The server is running on port 8000
    base_url = "http://127.0.0.1:8000"
    
    try:
        # Test the design generation endpoint
        # This simulates what the frontend called
        response = requests.post(f"{base_url}/api/design/generate", 
                               json={
                                   "room_id": "eb6176e1-63dd-475c-885c-18531e549fb8",
                                   "furniture_style": "modern",
                                   "wall_color": "white",
                                   "flooring_material": "hardwood"
                               },
                               headers={"Content-Type": "application/json"})
        
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print("✅ SUCCESS: Design generation worked!")
            print(f"Success: {data.get('success', False)}")
            
            if 'generated_images' in data:
                images = data['generated_images']
                print(f"Generated {len(images)} images:")
                for i, img in enumerate(images):
                    if img.startswith('data:image'):
                        print(f"  Image {i+1}: ✅ Real data URL ({len(img)} chars)")
                    else:
                        print(f"  Image {i+1}: {img[:50]}...")
            
            print(f"Engine: {data.get('engine_used', 'unknown')}")
            print(f"Time: {data.get('inference_time_seconds', 0):.2f}s")
            
        else:
            print(f"❌ FAILED: {response.status_code}")
            print(f"Response: {response.text}")
            
    except requests.exceptions.ConnectionError:
        print("❌ Server not running - start it first")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    test_design_generation_api()
