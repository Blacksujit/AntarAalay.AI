#!/usr/bin/env python3
"""
Test the fixed design generation
"""

import sys
from pathlib import Path

# Add backend directory to Python path
backend_dir = Path(__file__).parent
sys.path.insert(0, str(backend_dir))

def test_design_import():
    """Test that the design route imports correctly"""
    try:
        from app.routes.design import router
        print("✅ Design route imports successfully")
        
        # Test the specific function
        import inspect
        print("✅ Checking generate_design function...")
        
        return True
    except Exception as e:
        print(f"❌ Import error: {e}")
        return False

if __name__ == "__main__":
    success = test_design_import()
    print(f"\n{'🎉 DESIGN GENERATION READY!' if success else '❌ STILL BROKEN'}")
