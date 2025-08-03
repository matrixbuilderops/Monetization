#!/usr/bin/env python3
"""
Demo script to test the comprehensive validation system
"""

from code_quality_validator import CodeQualityValidator

def test_validation():
    """Test the comprehensive validation with sample code."""
    validator = CodeQualityValidator()
    
    # Test with code that has various issues
    test_code = '''
import os
import subprocess

def test_function():
    password = "hardcoded_password"
    exec("print('hello')")
    unused_variable = 42
    return eval("1+1")

if __name__ == "__main__":
    test_function()
'''
    
    print("🧪 Testing comprehensive validation with problematic code...")
    print("=" * 60)
    
    results = validator.validate_code(test_code, "test_demo.py")
    
    print("📊 Validation Results:")
    print(validator.get_summary(results))
    
    print("\n🔧 Improved Code:")
    print("-" * 40)
    print(results['improved_code'])
    print("-" * 40)
    
    print(f"\n📈 Total issues found: {len(results['issues'])}")
    print(f"📈 Total warnings: {len(results['warnings'])}")
    print(f"✅ Code is {'valid' if results['valid'] else 'invalid'}")

if __name__ == "__main__":
    test_validation()