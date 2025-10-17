#!/usr/bin/env python3
"""
Test runner for Trinity BRICKS
"""

import subprocess
import sys
import os

def run_tests():
    """Run the test suite with coverage."""
    print("🧪 Running Trinity BRICKS Test Suite...")
    print("=" * 50)
    
    # Change to backend directory
    os.chdir('/app')
    
    # Run pytest with coverage
    cmd = [
        'python', '-m', 'pytest',
        'tests/',
        '-v',
        '--cov=app',
        '--cov-report=term-missing',
        '--cov-report=html',
        '--tb=short'
    ]
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        print("STDOUT:")
        print(result.stdout)
        
        if result.stderr:
            print("STDERR:")
            print(result.stderr)
        
        print("=" * 50)
        print(f"Exit code: {result.returncode}")
        
        if result.returncode == 0:
            print("✅ All tests passed!")
        else:
            print("❌ Some tests failed!")
            
        return result.returncode
        
    except Exception as e:
        print(f"❌ Error running tests: {e}")
        return 1

if __name__ == "__main__":
    sys.exit(run_tests())
