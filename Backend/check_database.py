#!/usr/bin/env python3
"""
Check database for generated designs
"""

import sys
from pathlib import Path

# Add backend directory to Python path
backend_dir = Path(__file__).parent
sys.path.insert(0, str(backend_dir))

import sqlite3
import json

def check_database():
    """Check the database for generated designs"""
    
    print("🔍 Checking Database for Generated Designs")
    print("=" * 50)
    
    try:
        # Connect to the database
        conn = sqlite3.connect('antaralay.db')
        cursor = conn.cursor()
        
        # Check for designs
        cursor.execute("""
            SELECT id, room_id, user_id, style, budget, 
                   image_1_url, image_2_url, image_3_url,
                   created_at, status
            FROM designs 
            ORDER BY created_at DESC 
            LIMIT 5
        """)
        
        designs = cursor.fetchall()
        
        if designs:
            print(f"✅ Found {len(designs)} designs in database:")
            
            for design in designs:
                print(f"\n📋 Design ID: {design[0]}")
                print(f"   Room ID: {design[1]}")
                print(f"   User ID: {design[2]}")
                print(f"   Style: {design[3]}")
                print(f"   Budget: {design[4]}")
                print(f"   Status: {design[8]}")
                print(f"   Created: {design[7]}")
                
                # Check images
                images = [design[5], design[6], design[7]]
                real_images = [img for img in images if img and img.startswith('data:image')]
                print(f"   Real Images: {len(real_images)}/3")
                
                if real_images:
                    for i, img in enumerate(real_images):
                        print(f"     Image {i+1}: {len(img)} chars (data URL)")
        
        else:
            print("❌ No designs found in database")
        
        # Check the most recent room
        cursor.execute("""
            SELECT id, room_type, direction, created_at 
            FROM rooms 
            ORDER BY created_at DESC 
            LIMIT 1
        """)
        
        room = cursor.fetchone()
        if room:
            print(f"\n🏠 Latest Room: {room[0]}")
            print(f"   Type: {room[1]}")
            print(f"   Created: {room[3]}")
        
        conn.close()
        
    except Exception as e:
        print(f"❌ Database error: {e}")

if __name__ == "__main__":
    check_database()
