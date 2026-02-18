#!/usr/bin/env python3
"""
Fix import paths in all test files
"""

import sys
from pathlib import Path

backend_dir = Path(__file__).parent
tests_dir = backend_dir / "tests"

def fix_test_file(test_file):
    """Fix import paths in a test file."""
    try:
        content = test_file.read_text()
        
        # Check if already fixed
        if "backend_dir = Path(__file__).parent.parent.parent" in content:
            print(f"✅ {test_file.name} - Already fixed")
            return
        
        # Find the first import line
        lines = content.split('\n')
        insert_index = 0
        
        for i, line in enumerate(lines):
            if line.startswith('import ') or line.startswith('from '):
                insert_index = i
                break
        
        # Insert path setup code
        path_setup = [
            "import sys",
            "import os", 
            "from pathlib import Path",
            "",
            "# Add backend directory to Python path",
            "backend_dir = Path(__file__).parent.parent.parent",
            "sys.path.insert(0, str(backend_dir))",
            ""
        ]
        
        # Insert the path setup
        lines[insert_index:insert_index] = path_setup
        
        # Write back
        test_file.write_text('\n'.join(lines))
        print(f"✅ {test_file.name} - Fixed")
        
    except Exception as e:
        print(f"❌ {test_file.name} - Error: {e}")

def main():
    """Fix all test files."""
    print("🔧 Fixing import paths in test files...")
    
    # Fix unit tests
    unit_dir = tests_dir / "unit"
    for test_file in unit_dir.glob("test_*.py"):
        fix_test_file(test_file)
    
    # Fix integration tests
    integration_dir = tests_dir / "integration"
    for test_file in integration_dir.glob("test_*.py"):
        fix_test_file(test_file)
    
    print("\n🎉 All test files fixed!")

if __name__ == "__main__":
    main()
