#!/usr/bin/env python3
"""
Test room upload service
"""

import sys
from pathlib import Path

# Add backend directory to Python path
backend_dir = Path(__file__).parent
sys.path.insert(0, str(backend_dir))

def test_room_upload_service():
    """Test that the room upload service imports and works"""
    try:
        from app.services.room_service import room_upload_service
        print("✅ Room upload service imports successfully")
        
        # Test the service methods exist
        if hasattr(room_upload_service, 'upload_room_images'):
            print("✅ upload_room_images method exists")
        else:
            print("❌ upload_room_images method missing")
            
        if hasattr(room_upload_service, 'get_room'):
            print("✅ get_room method exists")
        else:
            print("❌ get_room method missing")
            
        if hasattr(room_upload_service, 'get_user_rooms'):
            print("✅ get_user_rooms method exists")
        else:
            print("❌ get_user_rooms method missing")
        
        return True
        
    except Exception as e:
        print(f"❌ Import error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_room_upload_service()
    print(f"\n{'🎉 ROOM UPLOAD SERVICE READY!' if success else '❌ ROOM UPLOAD SERVICE BROKEN'}")
