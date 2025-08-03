#!/usr/bin/env python3
"""
Interactive demo of the seamless generator without requiring Ollama.
Shows how the new generator handles different types of input.
"""

import sys
from pathlib import Path
from unittest.mock import patch

# Add current directory to path
sys.path.insert(0, str(Path(__file__).parent))

from python_code_generator_seamless import SeamlessPythonCodeGenerator

def mock_model_response(prompt):
    """Generate a mock response based on the prompt content."""
    
    # Extract the request from the prompt
    request_start = prompt.find('Request: ') + 9
    request_end = prompt.find('\n\nPython code:', request_start)
    
    if request_start > 8 and request_end > request_start:
        request = prompt[request_start:request_end].strip()
    else:
        request = "unknown request"
    
    # Generate appropriate mock code based on the request
    if "hello world" in request.lower():
        return '''def main():
    print("Hello, World!")

if __name__ == "__main__":
    main()'''
    
    elif "calculator" in request.lower():
        return '''def calculator():
    """Simple calculator program."""
    while True:
        try:
            num1 = float(input("Enter first number: "))
            operator = input("Enter operator (+, -, *, /): ")
            num2 = float(input("Enter second number: "))
            
            if operator == '+':
                result = num1 + num2
            elif operator == '-':
                result = num1 - num2
            elif operator == '*':
                result = num1 * num2
            elif operator == '/':
                result = num1 / num2
            else:
                print("Invalid operator")
                continue
                
            print(f"Result: {result}")
            
            if input("Continue? (y/n): ").lower() != 'y':
                break
        except ValueError:
            print("Invalid input, please try again.")
        except ZeroDivisionError:
            print("Cannot divide by zero!")

if __name__ == "__main__":
    calculator()'''
    
    elif "cats" in request.lower() or "stable diffusion" in request.lower():
        return '''#!/usr/bin/env python3
"""
Stable Diffusion Image Generator for CATS Categories
Generated from user request for comprehensive image generation script.
"""

import os
import random
from pathlib import Path
from typing import Dict, List

# User-configurable parameters
IMAGE_WIDTH = 2550
IMAGE_HEIGHT = 3300
IMAGES_PER_SUBCATEGORY = 6
OUTPUT_DIR = "stable_diffusion_images"
MODEL_ID = "stabilityai/stable-diffusion-2-1-base"
SEED = 42

# CATS dictionary as provided
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

def setup_cpu_mode():
    """Configure for CPU-only operation."""
    import torch
    torch.manual_seed(SEED)
    return torch.device("cpu")

def generate_images_for_category(category: str, subcategories: List[str], device):
    """Generate images for all subcategories in a category."""
    print(f"Processing category: {category}")
    
    for subcategory in subcategories:
        output_path = Path(OUTPUT_DIR) / subcategory
        output_path.mkdir(parents=True, exist_ok=True)
        
        for i in range(IMAGES_PER_SUBCATEGORY):
            image_filename = f"{subcategory}_{i+1:03d}.png"
            image_path = output_path / image_filename
            
            if image_path.exists():
                print(f"  Skipping existing: {image_path}")
                continue
            
            print(f"  Generating: {image_path}")
            # Here you would use the actual diffusion pipeline
            # For demo purposes, we'll just create a placeholder
            
def main():
    """Main execution function."""
    print("🎨 CATS Stable Diffusion Image Generator")
    print(f"Model: {MODEL_ID}")
    print(f"Resolution: {IMAGE_WIDTH}x{IMAGE_HEIGHT}")
    print(f"Images per subcategory: {IMAGES_PER_SUBCATEGORY}")
    print(f"Output directory: {OUTPUT_DIR}")
    print(f"Seed: {SEED}")
    print()
    
    device = setup_cpu_mode()
    
    for category, subcategories in CATS.items():
        generate_images_for_category(category, subcategories, device)
    
    print("✅ Image generation complete!")

if __name__ == "__main__":
    main()'''
    
    else:
        return f'''#!/usr/bin/env python3
"""
Python script generated for: {request[:100]}
"""

def main():
    """Main function for the generated script."""
    print("Script generated based on your request:")
    print("{request}")
    print("This is a placeholder - customize as needed!")

if __name__ == "__main__":
    main()'''

def demo_interactive_scenarios():
    """Run interactive demo scenarios."""
    
    print("🚀 Interactive Demo: Seamless Python Code Generator")
    print("=" * 60)
    print("This demo shows how the seamless generator handles different inputs")
    print("WITHOUT requiring Ollama (using mock responses for demonstration)")
    print("=" * 60)
    
    # Create generator instance
    generator = SeamlessPythonCodeGenerator()
    
    # Create a temporary output directory for demo
    demo_output = Path("demo_output")
    generator.set_output_directory(str(demo_output))
    
    scenarios = [
        {
            "name": "Simple Command",
            "input": "make a hello world program"
        },
        {
            "name": "Multi-line Calculator Request",
            "input": """create a calculator
that can do basic math operations
with error handling
and a user-friendly interface"""
        },
        {
            "name": "Complex CATS Dictionary Processing",
            "input": '''CATS = {
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

Generate a Python script using the Hugging Face diffusers library with the model 'stabilityai/stable-diffusion-2-1-base' to generate six images per subcategory. Use only CPU-compatible setup. The default image resolution must be 2550x3300 pixels (matching US Letter size at 300 DPI). Allow user-configurable parameters at the top of the script, such as image dimensions, number of images per subcategory (default: 6), output directory, and model ID. Use deterministic seed for reproducibility, skip generation if image already exists, and organize images under `stable_diffusion_images/<subcategory>/`.'''
        }
    ]
    
    # Mock the model call to avoid needing Ollama
    with patch.object(generator, 'call_model', side_effect=mock_model_response):
        
        for i, scenario in enumerate(scenarios, 1):
            print(f"\n📝 SCENARIO {i}: {scenario['name']}")
            print("-" * 40)
            
            input_preview = scenario['input'][:100] + "..." if len(scenario['input']) > 100 else scenario['input']
            print(f"Input: {input_preview}")
            print()
            
            print("🎯 Processing (this would normally call Ollama)...")
            
            # Process the request
            generator.process_request(scenario['input'])
            
            print(f"✅ Successfully generated script for scenario {i}")
            print()
    
    print("\n" + "=" * 60)
    print("📁 Generated Files:")
    print("=" * 60)
    
    if demo_output.exists():
        for file_path in demo_output.glob("*.py"):
            print(f"  📄 {file_path.name}")
            print(f"     Size: {file_path.stat().st_size} bytes")
    
    print("\n🎉 Demo Complete!")
    print("Key Benefits Demonstrated:")
    print("  ✅ No multi-line mode prompts")
    print("  ✅ Handles any input size seamlessly") 
    print("  ✅ Always generates ONE unified script")
    print("  ✅ Works with simple and complex requests equally")

if __name__ == "__main__":
    demo_interactive_scenarios()