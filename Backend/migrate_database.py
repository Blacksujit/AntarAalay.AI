#!/usr/bin/env python3
"""
Database migration script to add wall_color and flooring_material columns to designs table
"""

import sqlite3
import sys
from pathlib import Path

def migrate_database():
    """Add new columns to designs table"""
    db_path = Path(__file__).parent / "antaralay.db"
    
    if not db_path.exists():
        print(f"❌ Database not found: {db_path}")
        return False
    
    try:
        conn = sqlite3.connect(str(db_path))
        cursor = conn.cursor()
        
        # Check if columns already exist
        cursor.execute("PRAGMA table_info(designs)")
        columns = [column[1] for column in cursor.fetchall()]
        
        print(f"Current columns: {columns}")
        
        # Add wall_color column if not exists
        if 'wall_color' not in columns:
            print("Adding wall_color column...")
            cursor.execute("ALTER TABLE designs ADD COLUMN wall_color VARCHAR(50)")
            print("✅ wall_color column added")
        else:
            print("✅ wall_color column already exists")
        
        # Add flooring_material column if not exists
        if 'flooring_material' not in columns:
            print("Adding flooring_material column...")
            cursor.execute("ALTER TABLE designs ADD COLUMN flooring_material VARCHAR(50)")
            print("✅ flooring_material column added")
        else:
            print("✅ flooring_material column already exists")
        
        conn.commit()
        conn.close()
        
        print("\n🎉 Database migration completed successfully!")
        return True
        
    except Exception as e:
        print(f"❌ Migration failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = migrate_database()
    sys.exit(0 if success else 1)
