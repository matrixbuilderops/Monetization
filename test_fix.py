#!/usr/bin/env python3
"""
Test script to verify the Ollama command fix in ultimate_python_generator4_Version2.1.py
"""

import importlib.util
import sys
import subprocess
from unittest.mock import patch, MagicMock

# Load the fixed module
spec = importlib.util.spec_from_file_location('generator', 'ultimate_python_generator4_Version2.1.py')
module = importlib.util.module_from_spec(spec)
sys.modules['generator'] = module
spec.loader.exec_module(module)

def test_ollama_command_structure():
    """Test that the Ollama command is structured correctly."""
    print("🧪 Testing Ollama command structure...")
    
    generator = module.UltimatePythonCodeGenerator()
    
    # Mock subprocess.Popen to capture the command being used
    with patch('subprocess.Popen') as mock_popen:
        # Setup the mock to simulate successful execution
        mock_process = MagicMock()
        mock_process.communicate.return_value = ("test response", "")
        mock_process.returncode = 0
        mock_popen.return_value = mock_process
        
        # Call the model
        result = generator.call_model("test prompt")
        
        # Verify the command structure
        mock_popen.assert_called_once()
        call_args = mock_popen.call_args
        
        # Check the command arguments
        command = call_args[0][0]  # First positional argument
        expected_command = ['ollama', 'run', generator.model_name]
        
        if command == expected_command:
            print("✅ Command structure is correct: ['ollama', 'run', model_name]")
        else:
            print(f"❌ Command structure is wrong: {command}")
            return False
        
        # Check that stdin, stdout, stderr are configured for piping
        kwargs = call_args[1]  # Keyword arguments
        if (kwargs.get('stdin') == subprocess.PIPE and 
            kwargs.get('stdout') == subprocess.PIPE and 
            kwargs.get('stderr') == subprocess.PIPE):
            print("✅ Pipes are configured correctly for stdin/stdout/stderr")
        else:
            print(f"❌ Pipes not configured correctly: {kwargs}")
            return False
        
        # Check that communicate was called with the prompt
        mock_process.communicate.assert_called_once_with(input="test prompt", timeout=300)
        print("✅ Prompt is sent via stdin correctly")
        
        # Check the result
        if result == "test response":
            print("✅ Response handling is correct")
        else:
            print(f"❌ Response handling failed: {result}")
            return False
    
    return True

def test_error_handling():
    """Test error handling in the call_model method."""
    print("\n🧪 Testing error handling...")
    
    generator = module.UltimatePythonCodeGenerator()
    
    # Test FileNotFoundError (Ollama not installed)
    with patch('subprocess.Popen', side_effect=FileNotFoundError("ollama not found")):
        result = generator.call_model("test prompt")
        if result == "":
            print("✅ FileNotFoundError handled correctly")
        else:
            print(f"❌ FileNotFoundError not handled correctly: {result}")
            return False
    
    # Test non-zero return code
    with patch('subprocess.Popen') as mock_popen:
        mock_process = MagicMock()
        mock_process.communicate.return_value = ("", "error message")
        mock_process.returncode = 1
        mock_popen.return_value = mock_process
        
        result = generator.call_model("test prompt")
        if result == "":
            print("✅ Non-zero return code handled correctly")
        else:
            print(f"❌ Non-zero return code not handled correctly: {result}")
            return False
    
    return True

def test_comparison_with_working_version():
    """Compare with the working version to ensure consistency."""
    print("\n🧪 Comparing with working version...")
    
    # Load the working version
    spec_working = importlib.util.spec_from_file_location('working_generator', 'ultimate_python_generator.py')
    working_module = importlib.util.module_from_spec(spec_working)
    spec_working.loader.exec_module(working_module)
    
    fixed_generator = module.UltimatePythonCodeGenerator()
    working_generator = working_module.UltimatePythonCodeGenerator()
    
    # Both should use the same model
    if fixed_generator.model_name == working_generator.model_name:
        print(f"✅ Both versions use same model: {fixed_generator.model_name}")
    else:
        print(f"❌ Model mismatch: {fixed_generator.model_name} vs {working_generator.model_name}")
        return False
    
    print("✅ Basic compatibility with working version confirmed")
    return True

def main():
    """Run all tests."""
    print("🚀 Testing ultimate_python_generator4_Version2.1.py fixes")
    print("=" * 60)
    
    tests_passed = 0
    total_tests = 3
    
    if test_ollama_command_structure():
        tests_passed += 1
    
    if test_error_handling():
        tests_passed += 1
        
    if test_comparison_with_working_version():
        tests_passed += 1
    
    print("\n" + "=" * 60)
    print(f"Tests passed: {tests_passed}/{total_tests}")
    
    if tests_passed == total_tests:
        print("🎉 All tests passed! The fix is successful.")
        return True
    else:
        print("❌ Some tests failed. Please review the implementation.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)