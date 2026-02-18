#!/usr/bin/env python3
"""
Test factory integration with standalone engine
"""

import sys
from pathlib import Path

# Add backend directory to Python path
backend_dir = Path(__file__).parent
sys.path.insert(0, str(backend_dir))

from app.services.ai_engine import EngineFactory, EngineType

def test_factory():
    print("🔧 Testing Factory Integration")
    print("=" * 40)
    
    # Test LOCAL_SDXL (which should now use standalone)
    engine = EngineFactory.create_engine(EngineType.LOCAL_SDXL, {'device': 'cpu'})
    
    info = engine.get_model_info()
    print(f"✅ Engine Type: {info['engine_type']}")
    print(f"✅ Status: {info['status']}")
    print(f"✅ Features: {len(info['features'])} available")
    
    # Verify it's the standalone engine
    if 'Standalone' in info['engine_type']:
        print("✅ SUCCESS: Factory is using Standalone Engine!")
        return True
    else:
        print(f"❌ FAILURE: Factory is using {info['engine_type']}")
        return False

if __name__ == "__main__":
    success = test_factory()
    print(f"\n{'🎉 FACTORY INTEGRATION FIXED' if success else '❌ FACTORY INTEGRATION BROKEN'}")
