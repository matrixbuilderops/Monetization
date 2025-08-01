#!/usr/bin/env python3
"""
Test script to verify the timeout fix in python_code_generator.py
"""

import subprocess
import sys
import time
from pathlib import Path

def test_no_hard_timeout():
    """Test that the script doesn't have hard timeout limits."""
    print("🧪 Testing timeout fix...")
    
    # Test 1: Check that the script starts without immediate timeout
    try:
        process = subprocess.Popen(
            [sys.executable, "python_code_generator.py"],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        
        # Give it time to start
        time.sleep(2)
        
        # Send quit command
        stdout, stderr = process.communicate(input="quit\n", timeout=10)
        
        if "Interactive Python Code Generator" in stdout:
            print("✓ Script starts correctly")
        else:
            print("❌ Script startup issue")
            print("STDOUT:", stdout[:200])
            print("STDERR:", stderr[:200])
            return False
            
    except subprocess.TimeoutExpired:
        print("❌ Script took too long to respond")
        process.kill()
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False
    
    # Test 2: Check that script provides proper feedback for missing Ollama
    try:
        process = subprocess.Popen(
            [sys.executable, "python_code_generator.py"],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        
        # Send a request that would trigger model call
        stdout, stderr = process.communicate(
            input="make a hello world\nquit\n", 
            timeout=15  # Give more time for our enhanced feedback
        )
        
        # Check for expected behavior (no hard timeout message)
        if "Model call timed out" not in stdout:
            print("✓ No hard timeout message found")
        else:
            print("❌ Hard timeout message still present")
            return False
            
        if "Thinking" in stdout:
            print("✓ Enhanced thinking feedback present")
        else:
            print("❌ Missing enhanced thinking feedback")
            return False
            
        if "Press Ctrl+C to interrupt" in stdout:
            print("✓ User interruption guidance present")
        else:
            print("❌ Missing user interruption guidance")
            return False
            
    except subprocess.TimeoutExpired:
        print("❌ Script took too long for the test")
        process.kill()
        return False
    except Exception as e:
        print(f"❌ Unexpected error in test 2: {e}")
        return False
    
    print("🎉 All timeout fix tests passed!")
    return True

def test_demo_mode():
    """Test that demo mode still works."""
    print("\n🧪 Testing demo mode...")
    
    try:
        result = subprocess.run(
            [sys.executable, "demo_generator.py"],
            input="\n\n\n",  # Skip through demo prompts
            text=True,
            capture_output=True,
            timeout=30
        )
        
        if "Demo completed" in result.stdout:
            print("✓ Demo mode works correctly")
            return True
        else:
            print("❌ Demo mode issue")
            print("STDOUT:", result.stdout[:300])
            return False
            
    except subprocess.TimeoutExpired:
        print("❌ Demo mode timeout")
        return False
    except Exception as e:
        print(f"❌ Demo mode error: {e}")
        return False

if __name__ == "__main__":
    print("🚀 Running timeout fix verification tests...")
    print("=" * 50)
    
    success = True
    success &= test_no_hard_timeout()
    success &= test_demo_mode()
    
    print("\n" + "=" * 50)
    if success:
        print("🎉 All tests passed! Timeout fix is working correctly.")
        sys.exit(0)
    else:
        print("❌ Some tests failed. Please check the implementation.")
        sys.exit(1)