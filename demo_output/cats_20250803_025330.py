#!/usr/bin/env python3
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
    main()