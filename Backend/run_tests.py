#!/usr/bin/env python3
"""
Test Runner for AntarAalay.ai Backend

Runs all tests in the proper order:
1. Unit tests
2. Integration tests

Usage:
    python run_tests.py              # Run all tests
    python run_tests.py --unit       # Run only unit tests
    python run_tests.py --integration # Run only integration tests
    python run_tests.py --engine     # Run only engine tests
"""

import sys
import os
import subprocess
import argparse
from pathlib import Path

# Add the backend directory to Python path
backend_dir = Path(__file__).parent.absolute()
sys.path.insert(0, str(backend_dir))

# Set PYTHONPATH environment variable
os.environ['PYTHONPATH'] = str(backend_dir)

def run_unit_tests(test_filter=None):
    """Run unit tests."""
    print("🧪 Running Unit Tests")
    print("=" * 50)
    
    unit_dir = backend_dir / "tests" / "unit"
    
    if test_filter == "engine":
        test_files = [
            "test_gtx1650_config.py",
            "test_sd15_controlnet.py", 
            "test_ai_engine.py",
            "test_engine_no_token.py",
            "test_hf_engine.py",
            "test_free_engine.py",
            "test_interior_specific.py",
            "test_local_open_source.py",
            "test_real_token.py",
            "test_state_of_the_art.py"
        ]
    else:
        # Get all test files
        test_files = [f.name for f in unit_dir.glob("test_*.py")]
    
    success_count = 0
    total_count = len(test_files)
    
    for test_file in test_files:
        test_path = unit_dir / test_file
        print(f"\n🔍 Running {test_file}...")
        
        try:
            result = subprocess.run([
                sys.executable, str(test_path)
            ], capture_output=True, text=True, cwd=str(backend_dir))
            
            if result.returncode == 0:
                print(f"✅ {test_file} - PASSED")
                success_count += 1
                if result.stdout:
                    print(result.stdout)
            else:
                print(f"❌ {test_file} - FAILED")
                if result.stderr:
                    print(f"Error: {result.stderr}")
                if result.stdout:
                    print(result.stdout)
                    
        except Exception as e:
            print(f"❌ {test_file} - ERROR: {e}")
    
    print(f"\n📊 Unit Tests: {success_count}/{total_count} passed")
    return success_count == total_count

def run_integration_tests():
    """Run integration tests."""
    print("\n🔗 Running Integration Tests")
    print("=" * 50)
    
    integration_dir = backend_dir / "tests" / "integration"
    test_files = [f.name for f in integration_dir.glob("test_*.py")]
    
    success_count = 0
    total_count = len(test_files)
    
    for test_file in test_files:
        test_path = integration_dir / test_file
        print(f"\n🔍 Running {test_file}...")
        
        try:
            result = subprocess.run([
                sys.executable, str(test_path)
            ], capture_output=True, text=True, cwd=str(backend_dir))
            
            if result.returncode == 0:
                print(f"✅ {test_file} - PASSED")
                success_count += 1
                if result.stdout:
                    print(result.stdout)
            else:
                print(f"❌ {test_file} - FAILED")
                if result.stderr:
                    print(f"Error: {result.stderr}")
                    
        except Exception as e:
            print(f"❌ {test_file} - ERROR: {e}")
    
    print(f"\n📊 Integration Tests: {success_count}/{total_count} passed")
    return success_count == total_count

def main():
    """Main test runner."""
    parser = argparse.ArgumentParser(description="Run AntarAalay.ai Backend Tests")
    parser.add_argument("--unit", action="store_true", help="Run only unit tests")
    parser.add_argument("--integration", action="store_true", help="Run only integration tests")
    parser.add_argument("--engine", action="store_true", help="Run only engine tests")
    
    args = parser.parse_args()
    
    print("🏠 AntarAalay.ai Backend Test Runner")
    print("=" * 60)
    
    unit_success = True
    integration_success = True
    
    # Run tests based on arguments
    if args.unit or args.engine:
        unit_success = run_unit_tests("engine" if args.engine else None)
    elif args.integration:
        integration_success = run_integration_tests()
    else:
        # Run all tests
        unit_success = run_unit_tests()
        integration_success = run_integration_tests()
    
    # Final results
    print("\n" + "=" * 60)
    print("🏁 FINAL RESULTS")
    print("=" * 60)
    
    if unit_success and integration_success:
        print("🎉 ALL TESTS PASSED!")
        return 0
    else:
        print("❌ SOME TESTS FAILED!")
        if not unit_success:
            print("   - Unit tests failed")
        if not integration_success:
            print("   - Integration tests failed")
        return 1

if __name__ == "__main__":
    sys.exit(main())
