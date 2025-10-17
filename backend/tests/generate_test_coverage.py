#!/usr/bin/env python3
"""
Generate fresh test coverage data for AI code reviewer
This script runs the test suite and generates coverage.json
"""

import subprocess
import sys
import json
import os

def run_tests():
    """Run pytest with coverage and generate report"""
    print("🧪 Running test suite to generate fresh coverage data...")
    print("=" * 70)
    
    try:
        # Remove old coverage file
        if os.path.exists("coverage.json"):
            os.remove("coverage.json")
            print("✅ Removed old coverage file")
        
        # Run pytest with coverage
        result = subprocess.run(
            ["pytest", "--cov=app", "--cov-report=json", "--cov-report=term", "-v", "--tb=short"],
            capture_output=True,
            text=True,
            timeout=600  # 10 minute timeout
        )
        
        print(f"\n📊 Test execution completed (exit code: {result.returncode})")
        
        # Parse results
        import re
        tests_passed = 0
        tests_failed = 0
        
        if result.stdout:
            passed_match = re.search(r'(\d+)\s+passed', result.stdout)
            failed_match = re.search(r'(\d+)\s+failed', result.stdout)
            
            if passed_match:
                tests_passed = int(passed_match.group(1))
            if failed_match:
                tests_failed = int(failed_match.group(1))
        
        total_tests = tests_passed + tests_failed
        success_rate = (tests_passed / total_tests * 100) if total_tests > 0 else 0
        
        # Check coverage file
        if os.path.exists("coverage.json"):
            with open("coverage.json") as f:
                coverage_data = json.load(f)
            
            coverage_percent = coverage_data["totals"]["percent_covered"]
            
            print(f"\n✅ Test Results:")
            print(f"   Tests Passed: {tests_passed}/{total_tests} ({success_rate:.1f}%)")
            print(f"   Coverage: {coverage_percent:.1f}%")
            print(f"   Target: 80%")
            print(f"   Gap: {80 - coverage_percent:.1f}%")
            
            # Save summary
            summary = {
                "tests_passed": tests_passed,
                "tests_failed": tests_failed,
                "total_tests": total_tests,
                "success_rate": success_rate,
                "coverage_percent": coverage_percent,
                "meets_target": coverage_percent >= 80
            }
            
            with open("test_summary.json", "w") as f:
                json.dump(summary, f, indent=2)
            
            print(f"\n✅ Coverage data generated successfully!")
            print(f"   Files: coverage.json, test_summary.json")
            
            return 0
        else:
            print("\n❌ Coverage file not generated")
            print("Test output:")
            print(result.stdout[-1000:] if result.stdout else "No output")
            return 1
            
    except Exception as e:
        print(f"\n❌ Error running tests: {e}")
        return 1

if __name__ == "__main__":
    sys.exit(run_tests())

