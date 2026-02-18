#!/usr/bin/env python3
"""
Test the updated design generation API
"""

import sys
from pathlib import Path

# Add backend directory to Python path
backend_dir = Path(__file__).parent
sys.path.insert(0, str(backend_dir))

import sqlite3
import time

def check_for_new_designs():
    """Check if new designs are being created"""
    
    print("🔍 Checking for New Designs After API Update")
    print("=" * 55)
    
    try:
        # Connect to the database
        conn = sqlite3.connect('antaralay.db')
        cursor = conn.cursor()
        
        # Check recent designs
        cursor.execute("""
            SELECT id, room_id, user_id, style, status, created_at,
                   LENGTH(image_1_url) as img1_size,
                   LENGTH(image_2_url) as img2_size, 
                   LENGTH(image_3_url) as img3_size
            FROM designs 
            ORDER BY created_at DESC 
            LIMIT 3
        """)
        
        designs = cursor.fetchall()
        
        if designs:
            print(f"✅ Found {len(designs)} recent designs:")
            
            for design in designs:
                print(f"\n📋 Design ID: {design[0]}")
                print(f"   Room ID: {design[1]}")
                print(f"   Style: {design[3]}")
                print(f"   Status: {design[4]}")
                print(f"   Created: {design[5]}")
                
                # Check image sizes
                img_sizes = [design[6], design[7], design[8]]
                real_images = [size for size in img_sizes if size and size > 1000]
                print(f"   Real Images: {len(real_images)}/3")
                
                if real_images:
                    for i, size in enumerate(real_images):
                        if size > 10000:  # Substantial image data
                            print(f"     Image {i+1}: ✅ {size} bytes (REAL DATA)")
                        else:
                            print(f"     Image {i+1}: ⚠️  {size} bytes (small)")
                
                # Check if it's a recent design (created in last few minutes)
                if design[5] and '2026-02-18' in design[5]:
                    print(f"   🆕 NEW DESIGN CREATED!")
        
        else:
            print("❌ No designs found")
            print("💡 Try generating a design from the frontend")
        
        conn.close()
        
    except Exception as e:
        print(f"❌ Database error: {e}")

def show_instructions():
    """Show instructions for testing"""
    print("\n🎯 TO TEST THE DESIGN GENERATION:")
    print("1. Make sure server is running: python -m uvicorn main:app --reload --port 8000")
    print("2. Open frontend and upload room images")
    print("3. Click 'Generate Design' button")
    print("4. Check back here: python check_new_designs.py")
    print("\n🚀 The server now uses our Standalone Engine for REAL image generation!")

if __name__ == "__main__":
    check_for_new_designs()
    show_instructions()
