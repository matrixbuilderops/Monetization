#!/usr/bin/env python3
"""
Test script for enhanced_python_generator8.py
Validates syntax error fixes and prompt parsing capabilities.
"""

import sys
import os
from pathlib import Path

# Add the current directory to path
sys.path.insert(0, str(Path(__file__).parent))

try:
    from enhanced_python_generator8 import EnhancedPythonGenerator8
    print("✅ Successfully imported enhanced_python_generator8")
except ImportError as e:
    print(f"❌ Failed to import: {e}")
    sys.exit(1)

def test_syntax_error_fix():
    """Test that the generator can fix unterminated string literals."""
    print("\n🧪 Testing syntax error fixes...")
    
    generator = EnhancedPythonGenerator8()
    
    # Test unterminated string fix
    broken_code = '''def test():
    pattern3 = r'\\s+([a-zA-Z_][a-zA-Z0-9_]*\\.py)
    return pattern3'''
    
    fixed_code = generator._fix_unterminated_strings(broken_code)
    
    # Check if the string was properly closed
    if "pattern3 = r'\\s+([a-zA-Z_][a-zA-Z0-9_]*\\.py)'" in fixed_code:
        print("✅ Unterminated string literal fixed successfully")
    else:
        print("❌ Failed to fix unterminated string literal")
        print(f"Result: {fixed_code}")

def test_prompt_parsing():
    """Test complex prompt parsing."""
    print("\n🧪 Testing prompt parsing...")
    
    generator = EnhancedPythonGenerator8()
    
    # Test the example prompt from the problem statement
    test_prompt = '''I want you to make a script that makes stable diffusion that is based of all these categories which are in the [] the script should make a folder for categories in front of the [] such as productivity. The script should allow me to pick the categories if I want to do it like that or do all of them. It should also allow me to pick a different size of the output with the standard size being a sheet of paper 550x3300 pixels (matching US Letter size at 300 DPI). Also the script should make 6 images per category. CATEGORIES = {
    "productivity": ["burnout", "focus", "time_management", "imposter_syndrome"],
    "confidence": ["self-esteem", "public_speaking", "courage"],
    "gratitude": ["daily_gratitude", "thankfulness"]
}'''
    
    result = generator.parse_complex_prompt(test_prompt)
    
    # Validate parsing results
    checks = [
        (result['script_type'] == 'stable_diffusion', "Script type detection"),
        (result['output_specs']['width'] == 550, "Width parsing"),
        (result['output_specs']['height'] == 3300, "Height parsing"),
        (result['output_specs']['images_per_category'] == 6, "Images per category parsing"),
        (len(result['categories']) == 3, "Category count"),
        ('productivity' in result['categories'], "Category parsing"),
        ('folder_organization' in result['features'], "Feature detection")
    ]
    
    for check, description in checks:
        if check:
            print(f"✅ {description}")
        else:
            print(f"❌ {description}")
            print(f"   Result: {result}")

def test_code_generation():
    """Test code generation functionality."""
    print("\n🧪 Testing code generation...")
    
    generator = EnhancedPythonGenerator8()
    
    simple_prompt = "Create a hello world script"
    
    try:
        code = generator.generate_code(simple_prompt)
        if "def main():" in code or "print(" in code:
            print("✅ Basic code generation works")
        else:
            print("❌ Code generation failed")
            print(f"Generated: {code[:200]}...")
    except Exception as e:
        print(f"❌ Code generation error: {e}")

def main():
    """Run all tests."""
    print("🚀 Testing Enhanced Python Generator 8")
    print("=" * 50)
    
    test_syntax_error_fix()
    test_prompt_parsing()
    test_code_generation()
    
    print("\n✅ All tests completed!")

if __name__ == "__main__":
    main()