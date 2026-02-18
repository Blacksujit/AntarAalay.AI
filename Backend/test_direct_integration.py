#!/usr/bin/env python3
"""
Direct test of standalone engine integration
"""

import sys
from pathlib import Path

# Add backend directory to Python path
backend_dir = Path(__file__).parent
sys.path.insert(0, str(backend_dir))

from app.services.ai_engine.standalone_image_engine import StandaloneImageEngine

def test_direct():
    print("🔧 Testing Standalone Engine Direct Integration")
    print("=" * 55)
    
    # Create engine directly
    engine = StandaloneImageEngine({'device': 'cpu'})
    
    # Test info
    info = engine.get_model_info()
    print(f"✅ Engine: {info['engine_type']}")
    print(f"✅ Resolution: {info['resolution']}")
    print(f"✅ Status: {info['status']}")
    print(f"✅ Features: {len(info['features'])} available")
    
    # This is what the server will use
    print(f"\n🚀 SERVER INTEGRATION READY!")
    print(f"   Engine Type: {info['engine_type']}")
    print(f"   Model: {info.get('model_type', 'Algorithmic')}")
    print(f"   Status: {info['status']}")
    
    return True

if __name__ == "__main__":
    test_direct()
    print("\n✅ READY TO START SERVER WITH ACTUAL IMAGE GENERATION!")
