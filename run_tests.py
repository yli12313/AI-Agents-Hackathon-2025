#!/usr/bin/env python3
"""
Test runner script for Streamlit chatbot access tests.
This script provides an easy way to run all tests with proper configuration.
"""

import os
import sys
import subprocess
import argparse

def run_tests(verbose=False, coverage=False, specific_test=None):
    """Run the test suite."""
    
    # Ensure we're in the right directory
    script_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(script_dir)
    
    # Base pytest command
    cmd = ["python3", "-m", "pytest"]
    
    if verbose:
        cmd.append("-v")
    
    if coverage:
        cmd.extend(["--cov=streamlit", "--cov-report=html", "--cov-report=term"])
    
    # Add specific test file or pattern
    if specific_test:
        cmd.append(specific_test)
    else:
        cmd.append("test_streamlit_chatbot.py")
    
    print(f"Running command: {' '.join(cmd)}")
    print("=" * 50)
    
    try:
        result = subprocess.run(cmd, check=True)
        print("\n" + "=" * 50)
        print("✅ All tests passed!")
        return True
    except subprocess.CalledProcessError as e:
        print("\n" + "=" * 50)
        print(f"❌ Tests failed with exit code {e.returncode}")
        return False
    except FileNotFoundError:
        print("❌ pytest not found. Please install dependencies:")
        print("   pip install -r requirements.txt")
        return False

def main():
    """Main entry point."""
    description = "Run Streamlit chatbot access tests"
    parser = argparse.ArgumentParser(description)
    
    parser.add_argument(
        "-v", "--verbose", 
        action="store_true", 
        help="Verbose output"
    )
    
    parser.add_argument(
        "-c", "--coverage", 
        action="store_true", 
        help="Enable coverage reporting"
    )
    
    parser.add_argument(
        "-t", "--test", 
        type=str, 
        help="Run specific test file or pattern"
    )
    
    args = parser.parse_args()
    
    success = run_tests(
        verbose=args.verbose,
        coverage=args.coverage,
        specific_test=args.test
    )
    
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()
