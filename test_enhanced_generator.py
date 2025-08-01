#!/usr/bin/env python3
"""
Test script for the enhanced Python code generator.
Demonstrates how to properly input complex data structures like the CATS dictionary.
"""

def create_sample_cats_request():
    """Create a sample CATS dictionary request that should generate a single comprehensive script."""
    
    cats_request = '''Create a comprehensive Python script using this CATS dictionary:

CATS = {
    "productivity": ["imposter_syndrome", "burnout", "workspace_focus"],
    "confidence": ["self_doubt", "public_speaking", "decision_making"],
    "gratitude": ["daily_practice", "gratitude_after_loss", "gratitude_for_body"],
    "healing": ["breakup", "trauma", "loss"],
    "focus": ["ADHD", "study_block", "digital_distraction"],
    "creativity": ["artist_block", "new_idea", "creative_confidence"],
    "happiness": ["moment_to_moment", "joyful_small_things", "inner_child"],
    "resilience": ["setback_recovery", "stress_response", "mental_toughness"],
    "self_love": ["body_image", "self_acceptance", "personal_growth"],
    "stress_relief": ["deep_breathing", "tension_release", "deadline_pressure"],
    "success": ["goals_alignment", "career_vision", "achievement_mindset"],
    "anxiety_relief": ["panic_attack", "social_anxiety", "future_worry"],
    "mindfulness": ["present_awareness", "grounding", "calm_presence"],
    "motivation": ["morning_boost", "daily_grind", "persistence"],
    "relationships": ["toxic_family", "romantic_conflict", "friendship_loss"]
}

Build a Python script that uses the Hugging Face diffusers library with the model 'stabilityai/stable-diffusion-2-1-base' to generate six images per subcategory. Use only CPU-compatible setup. The default image resolution must be 2550x3300 pixels (matching US Letter size at 300 DPI). Allow user-configurable parameters at the top of the script, such as image dimensions, number of images per subcategory (default: 6), output directory, and model ID. Use deterministic seed for reproducibility, skip generation if image already exists, and organize images under `stable_diffusion_images/<subcategory>/`.'''
    
    return cats_request

def create_multi_line_test():
    """Create a multi-line input test to demonstrate the enhanced input handling."""
    
    lines = [
        'CATS = {',
        '    "productivity": ["imposter_syndrome", "burnout", "workspace_focus"],',
        '    "confidence": ["self_doubt", "public_speaking", "decision_making"],',
        '    "gratitude": ["daily_practice", "gratitude_after_loss", "gratitude_for_body"]',
        '}',
        '',
        'Generate a script that processes this dictionary and creates affirmation bundles for each category.'
    ]
    
    return lines

def test_structure_detection():
    """Test the structure detection functionality."""
    from python_code_generator_enhanced import EnhancedPythonCodeGenerator
    
    generator = EnhancedPythonCodeGenerator()
    
    test_cases = [
        'CATS = {',
        '"productivity": ["imposter_syndrome", "burnout"],',
        'hello world',
        '{"key": "value"',
        'make a calculator'
    ]
    
    print("Testing structure detection:")
    print("-" * 40)
    
    for test_case in test_cases:
        is_incomplete = generator.is_incomplete_structure(test_case)
        structure_type = generator.detect_data_structure_type(test_case)
        print(f"Input: {test_case}")
        print(f"  Incomplete: {is_incomplete}")
        print(f"  Type: {structure_type}")
        print()

if __name__ == "__main__":
    print("🧪 Test Script for Enhanced Python Code Generator")
    print("=" * 50)
    
    print("\n1. Testing structure detection:")
    test_structure_detection()
    
    print("\n2. Sample complete CATS request:")
    print("-" * 30)
    sample_request = create_sample_cats_request()
    print(f"Length: {len(sample_request)} characters")
    print("Preview:", sample_request[:200] + "...")
    
    print("\n3. Sample multi-line input:")
    print("-" * 30)
    multi_line_test = create_multi_line_test()
    for i, line in enumerate(multi_line_test, 1):
        print(f"Line {i}: {line}")
    
    print("\n4. Usage Instructions:")
    print("-" * 30)
    print("To test the enhanced generator:")
    print("1. Run: python3 python_code_generator_enhanced.py")
    print("2. Enter the complete CATS request as one input")
    print("3. Or start typing 'CATS = {' and let it detect multi-line mode")
    print("4. The generator should create ONE comprehensive script, not multiple files")