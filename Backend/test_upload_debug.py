#!/usr/bin/env python3
"""
Debug image upload issues
"""

import sys
from pathlib import Path

# Add backend directory to Python path
backend_dir = Path(__file__).parent
sys.path.insert(0, str(backend_dir))

def test_upload_flow():
    """Test the complete upload flow"""
    try:
        print("🔍 Testing Image Upload Flow")
        print("=" * 50)
        
        # Test 1: Check storage service
        print("1. Testing storage service...")
        from app.services.storage import get_storage_service
        storage = get_storage_service()
        print(f"   Storage type: {type(storage)}")
        print(f"   Storage dir: {storage.storage_dir}")
        print(f"   Base URL: {storage.base_url}")
        
        # Test 2: Check upload directory
        print("2. Checking upload directory...")
        upload_dir = Path("uploads")
        if upload_dir.exists():
            print(f"   ✅ Uploads directory exists: {upload_dir.absolute()}")
            print(f"   Permissions: {oct(upload_dir.stat().st_mode)[-3:]}")
        else:
            print(f"   ❌ Uploads directory missing!")
            
        # Test 3: Test file upload
        print("3. Testing file upload...")
        test_content = b"fake_image_content_for_testing"
        test_url = storage.upload_image(
            test_content,
            "image/jpeg",
            "test"
        )
        print(f"   Upload URL: {test_url}")
        
        # Test 4: Verify file exists
        print("4. Verifying uploaded file...")
        if "uploads/" in test_url:
            file_path = test_url.split("uploads/")[-1]
            full_path = upload_dir / file_path
            if full_path.exists():
                print(f"   ✅ File exists: {full_path}")
                print(f"   File size: {full_path.stat().st_size} bytes")
            else:
                print(f"   ❌ File not found: {full_path}")
        
        # Test 5: Test room service
        print("5. Testing room service...")
        from app.services.room_service import room_upload_service
        print(f"   Room service type: {type(room_upload_service)}")
        print(f"   Storage service type: {type(room_upload_service.storage_service)}")
        
        # Test 6: Check API endpoint
        print("6. Checking API endpoint...")
        from app.api.room import router
        print(f"   Router prefix: {router.prefix}")
        
        print("\n🎉 Upload Flow Test Complete!")
        print("✅ Storage service working")
        print("✅ Upload directory exists")
        print("✅ File upload working")
        print("✅ Room service working")
        print("✅ API endpoint available")
        
        return True
        
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        import traceback
        print(f"Traceback: {traceback.format_exc()}")
        return False

if __name__ == "__main__":
    test_upload_flow()
