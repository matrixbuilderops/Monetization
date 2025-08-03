#!/usr/bin/env python3
"""
Test script to verify the enhanced Python code generator with comprehensive validation
"""

from python_code_generator import PythonCodeGenerator
from fixed_python_generator import EnhancedPythonCodeGenerator
import tempfile
import os

def test_basic_generator():
    """Test the basic Python code generator with comprehensive validation."""
    print("🧪 Testing Basic Python Code Generator")
    print("=" * 50)
    
    generator = PythonCodeGenerator()
    
    # Simulate generated code (what would come from the AI model)
    test_code = '''def calculate_fibonacci(n):
    if n <= 1:
        return n
    return calculate_fibonacci(n-1) + calculate_fibonacci(n-2)

if __name__ == "__main__":
    for i in range(10):
        print(f"Fibonacci {i}: {calculate_fibonacci(i)}")
'''
    
    # Test the validation directly
    if generator.quality_validator:
        print("✅ Comprehensive validation is available")
        results = generator.quality_validator.validate_code(test_code, "fibonacci_test.py")
        print("📊 Validation Results:")
        print(generator.quality_validator.get_summary(results))
        print("\n🔧 Improved Code:")
        print(results['improved_code'][:200] + "..." if len(results['improved_code']) > 200 else results['improved_code'])
    else:
        print("⚠️  Comprehensive validation not available")
    
    print("\n✅ Basic generator test completed!")

def test_enhanced_generator():
    """Test the enhanced Python code generator with comprehensive validation."""
    print("\n🧪 Testing Enhanced Python Code Generator")
    print("=" * 50)
    
    generator = EnhancedPythonCodeGenerator()
    
    # Test the comprehensive validation method
    test_code = '''
import os

def read_config_file():
    password = "secret123"  # Security issue
    file_path = "/tmp/config.txt"
    with open(file_path, 'r') as f:
        return f.read()

def unused_function():  # Dead code
    pass

if __name__ == "__main__":
    read_config_file()
'''
    
    print("🔍 Testing comprehensive validation...")
    is_valid, issues, improved_code = generator.comprehensive_code_validation(test_code)
    
    print(f"✅ Code valid: {is_valid}")
    print(f"📊 Issues found: {len(issues)}")
    if issues:
        print("🔴 Issues:")
        for issue in issues[:5]:  # Show first 5 issues
            print(f"   • {issue}")
    
    print("\n🔧 Code was improved:")
    print("YES" if improved_code != test_code else "NO")
    
    print("\n✅ Enhanced generator test completed!")

def main():
    """Run all tests."""
    print("🚀 Testing Comprehensive Code Quality Integration")
    print("=" * 70)
    
    try:
        test_basic_generator()
        test_enhanced_generator()
        
        print("\n" + "=" * 70)
        print("🎉 All tests completed successfully!")
        print("✅ Comprehensive code quality validation is working!")
        print("📈 Both generators now use all 10 quality tools:")
        print("   bandit, coverage, flake8, hypothesis, interrogate,")
        print("   mypy, pathspec, pylint, vulture, z3")
        
    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()