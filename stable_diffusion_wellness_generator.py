#!/usr/bin/env python3
"""
Comprehensive Stable Diffusion Wellness Image Generator

This script generates images for wellness and affirmation categories using Stable Diffusion.
All categories are processed in a single, unified script - no fragmentation!

Features:
- Configurable paper size output (default: US Letter 2550x3300 at 300 DPI)
- CPU-compatible setup
- Skip existing files to avoid regeneration
- Deterministic seed for reproducibility
- Organized output structure
- Comprehensive wellness prompts (NOT about cats!)
"""

import os
import random
import json
import argparse
from pathlib import Path
from typing import Dict, List, Tuple
from datetime import datetime

# Try to import the required libraries
try:
    import torch
    from diffusers import StableDiffusionPipeline
    from PIL import Image
    DIFFUSERS_AVAILABLE = True
except ImportError:
    print("⚠️  Diffusers not available. Running in simulation mode.")
    DIFFUSERS_AVAILABLE = False

# ========================= USER CONFIGURATION =========================
# Modify these settings to customize the image generation

# Image settings - Default: US Letter size at 300 DPI
IMAGE_WIDTH = 2550  # US Letter width at 300 DPI
IMAGE_HEIGHT = 3300  # US Letter height at 300 DPI

# Generation settings
IMAGES_PER_SUBCATEGORY = 6  # Number of images to generate per subcategory
OUTPUT_BASE_DIR = "stable_diffusion_images"  # Base output directory
MODEL_ID = "stabilityai/stable-diffusion-2-1-base"  # Stable Diffusion model
DETERMINISTIC_SEED = 42  # For reproducible results
DEVICE = "cpu"  # Use CPU for compatibility
NUM_INFERENCE_STEPS = 20  # Faster generation with fewer steps

# Advanced settings
SKIP_EXISTING = True  # Skip generating images that already exist
SAVE_PROMPTS = True  # Save prompts to text files alongside images
BATCH_SIZE = 1  # Process one image at a time for stability

# ===================== WELLNESS CATEGORIES DICTIONARY =====================
# This is the proper CATS dictionary for wellness/affirmation categories
# NOT about feline cats - these are wellness and personal development categories!

WELLNESS_CATEGORIES = {
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

class WellnessImageGenerator:
    """Comprehensive generator for wellness and affirmation images."""
    
    def __init__(self, config=None):
        """Initialize the wellness image generator."""
        self.config = config or {}
        self.model_id = self.config.get('model_id', MODEL_ID)
        self.device = self.config.get('device', DEVICE)
        self.seed = self.config.get('seed', DETERMINISTIC_SEED)
        self.image_width = self.config.get('width', IMAGE_WIDTH)
        self.image_height = self.config.get('height', IMAGE_HEIGHT)
        self.images_per_subcategory = self.config.get('count', IMAGES_PER_SUBCATEGORY)
        self.output_dir = Path(self.config.get('output', OUTPUT_BASE_DIR))
        self.skip_existing = self.config.get('skip_existing', SKIP_EXISTING)
        
        # Set random seeds for reproducibility
        random.seed(self.seed)
        if DIFFUSERS_AVAILABLE:
            torch.manual_seed(self.seed)
        
        # Initialize statistics
        self.stats = {
            "total_categories": len(WELLNESS_CATEGORIES),
            "total_subcategories": sum(len(subcats) for subcats in WELLNESS_CATEGORIES.values()),
            "total_images_planned": sum(len(subcats) for subcats in WELLNESS_CATEGORIES.values()) * self.images_per_subcategory,
            "images_generated": 0,
            "images_skipped": 0,
            "start_time": datetime.now()
        }
        
        # Initialize the pipeline
        self.pipeline = None
        if DIFFUSERS_AVAILABLE:
            self._initialize_pipeline()
        
        # Create output directory
        self.output_dir.mkdir(exist_ok=True, parents=True)
        print(f"✓ Output directory: {self.output_dir.absolute()}")
    
    def _initialize_pipeline(self):
        """Initialize the Stable Diffusion pipeline."""
        try:
            print(f"🔄 Loading Stable Diffusion model: {self.model_id}")
            self.pipeline = StableDiffusionPipeline.from_pretrained(
                self.model_id,
                torch_dtype=torch.float32,  # Use float32 for CPU compatibility
                safety_checker=None,
                requires_safety_checker=False
            )
            
            # Move to specified device
            self.pipeline = self.pipeline.to(self.device)
            
            # Enable memory efficient attention for CPU
            if self.device == "cpu":
                self.pipeline.enable_attention_slicing(1)
            
            print(f"✓ Model loaded successfully on {self.device}")
            
        except Exception as e:
            print(f"❌ Error loading pipeline: {e}")
            print("📝 Running in simulation mode")
            self.pipeline = None
    
    def create_wellness_prompt(self, category: str, subcategory: str) -> str:
        """Generate appropriate prompts for wellness and affirmation categories."""
        
        # Define wellness-focused prompt templates
        prompt_templates = {
            "productivity": {
                "imposter_syndrome": "A confident professional workspace scene, overcoming self-doubt, warm inspiring lighting, motivational atmosphere, clean modern aesthetic",
                "burnout": "A peaceful restoration scene, work-life balance, serene natural environment, healing energy, soft calming colors",
                "workspace_focus": "An organized, distraction-free workspace, clear focus energy, minimalist design, productive atmosphere"
            },
            "confidence": {
                "self_doubt": "An empowering scene of personal strength, inner confidence radiating, golden hour lighting, uplifting composition",
                "public_speaking": "A confident speaker in a supportive environment, positive energy, encouraging atmosphere, professional setting",
                "decision_making": "A clear path forward, decisive moment, strong leadership energy, confident posture, inspiring backdrop"
            },
            "gratitude": {
                "daily_practice": "A peaceful morning gratitude ritual, thankful meditation, soft natural light, harmonious composition",
                "gratitude_after_loss": "A gentle healing scene, finding beauty in difficult times, soft pastels, comforting atmosphere",
                "gratitude_for_body": "Body appreciation and self-care, healthy lifestyle imagery, positive body energy, nurturing environment"
            },
            "healing": {
                "breakup": "Emotional healing and new beginnings, gentle recovery energy, soft healing colors, peaceful solitude",
                "trauma": "Safe healing space, therapeutic environment, gentle recovery process, protective warm lighting",
                "loss": "Gentle grief processing, remembrance and healing, soft memorial energy, comforting atmosphere"
            },
            "focus": {
                "ADHD": "Clear mental organization, structured thinking space, calm focused energy, distraction-free environment",
                "study_block": "Breakthrough learning moment, academic inspiration, clear thinking energy, productive study space",
                "digital_distraction": "Mindful technology use, focused attention, present moment awareness, calm productivity"
            },
            "creativity": {
                "artist_block": "Creative breakthrough, artistic inspiration flowing, vibrant creative energy, inspiring studio space",
                "new_idea": "Innovation and fresh thinking, lightbulb moment, creative spark, inspiring ideation environment",
                "creative_confidence": "Artistic self-expression, creative courage, bold artistic energy, inspiring creative space"
            },
            "happiness": {
                "moment_to_moment": "Present moment joy, mindful happiness, simple pleasures, warm joyful lighting",
                "joyful_small_things": "Finding joy in everyday moments, simple happiness, cheerful atmosphere, uplifting details",
                "inner_child": "Playful joy and wonder, childlike happiness, carefree energy, bright playful colors"
            },
            "resilience": {
                "setback_recovery": "Bouncing back stronger, resilient spirit, overcoming challenges, determined energy",
                "stress_response": "Calm under pressure, steady resilience, grounded strength, stable foundation",
                "mental_toughness": "Inner strength and durability, unshakeable spirit, strong mental fortitude, stable energy"
            },
            "self_love": {
                "body_image": "Body appreciation and acceptance, positive self-image, loving self-care, nurturing environment",
                "self_acceptance": "Embracing authenticity, self-compassion, gentle self-love, accepting peaceful energy",
                "personal_growth": "Evolution and self-improvement, growth mindset, transformative energy, inspiring progress"
            },
            "stress_relief": {
                "deep_breathing": "Calming breath work, peaceful respiratory flow, meditative breathing, tranquil atmosphere",
                "tension_release": "Physical and mental relaxation, stress melting away, soothing relief, peaceful release",
                "deadline_pressure": "Calm productivity under pressure, organized efficiency, stress-free achievement, composed energy"
            },
            "success": {
                "goals_alignment": "Clear vision and purpose, aligned objectives, focused direction, inspiring goal achievement",
                "career_vision": "Professional aspiration and growth, career inspiration, ambitious energy, success pathway",
                "achievement_mindset": "Victory and accomplishment, winning attitude, successful completion, triumphant energy"
            },
            "anxiety_relief": {
                "panic_attack": "Calm breathing and safety, anxiety relief, peaceful grounding, secure comforting environment",
                "social_anxiety": "Comfortable social connection, confident interaction, supportive community, welcoming atmosphere",
                "future_worry": "Present moment peace, releasing future anxiety, calm certainty, grounded stability"
            },
            "mindfulness": {
                "present_awareness": "Mindful present moment, conscious awareness, meditative presence, centered peaceful energy",
                "grounding": "Earth connection and stability, grounded presence, natural grounding energy, rooted strength",
                "calm_presence": "Serene mindful state, peaceful awareness, tranquil presence, meditative calm"
            },
            "motivation": {
                "morning_boost": "Energizing sunrise motivation, fresh start energy, inspiring morning ritual, uplifting beginning",
                "daily_grind": "Consistent daily progress, steady motivation, persistent effort, determined daily energy",
                "persistence": "Never giving up, enduring motivation, persistent drive, unwavering determination"
            },
            "relationships": {
                "toxic_family": "Healthy boundaries and healing, family recovery, protective self-care, supportive healing environment",
                "romantic_conflict": "Relationship healing and communication, love restoration, peaceful resolution, harmonious connection",
                "friendship_loss": "Social healing and new connections, friendship recovery, supportive community, welcoming social energy"
            }
        }
        
        # Get specific prompt or create a generic one
        if category in prompt_templates and subcategory in prompt_templates[category]:
            base_prompt = prompt_templates[category][subcategory]
        else:
            base_prompt = f"A supportive wellness scene for {subcategory.replace('_', ' ')}, healing energy, peaceful atmosphere, inspiring composition"
        
        # Add style and quality modifiers
        style_additions = ", high quality, professional photography, soft lighting, peaceful composition, wellness aesthetic, therapeutic art style"
        
        return base_prompt + style_additions
    
    def image_exists(self, category: str, subcategory: str, image_index: int) -> bool:
        """Check if an image already exists."""
        image_path = self.output_dir / subcategory / f"{category}_{subcategory}_{image_index:02d}.png"
        return image_path.exists() if self.skip_existing else False
    
    def save_prompt_file(self, category: str, subcategory: str, image_index: int, prompt: str):
        """Save the prompt to a text file alongside the image."""
        if SAVE_PROMPTS:
            prompt_path = self.output_dir / subcategory / f"{category}_{subcategory}_{image_index:02d}_prompt.txt"
            with open(prompt_path, 'w') as f:
                f.write(f"Category: {category}\n")
                f.write(f"Subcategory: {subcategory}\n")
                f.write(f"Image Index: {image_index}\n")
                f.write(f"Generated: {datetime.now().isoformat()}\n")
                f.write(f"Model: {self.model_id}\n")
                f.write(f"Dimensions: {self.image_width}x{self.image_height}\n")
                f.write(f"Seed: {self.seed}\n\n")
                f.write(f"Prompt:\n{prompt}\n")
    
    def generate_image(self, prompt: str, category: str, subcategory: str, image_index: int) -> bool:
        """Generate a single image."""
        image_filename = f"{category}_{subcategory}_{image_index:02d}.png"
        subcategory_dir = self.output_dir / subcategory
        subcategory_dir.mkdir(exist_ok=True, parents=True)
        image_path = subcategory_dir / image_filename
        
        try:
            if self.pipeline:
                # Generate image with Stable Diffusion
                with torch.no_grad():
                    result = self.pipeline(
                        prompt,
                        height=self.image_height,
                        width=self.image_width,
                        num_inference_steps=NUM_INFERENCE_STEPS,
                        guidance_scale=7.5,
                        generator=torch.Generator(device=self.device).manual_seed(self.seed + image_index)
                    )
                    image = result.images[0]
                    image.save(image_path)
            else:
                # Simulation mode - create placeholder
                try:
                    from PIL import Image, ImageDraw, ImageFont
                except ImportError:
                    # Create a simple text placeholder if PIL is not available
                    with open(image_path.with_suffix('.txt'), 'w') as f:
                        f.write(f"WELLNESS IMAGE PLACEHOLDER\n")
                        f.write(f"Category: {category}\n")
                        f.write(f"Subcategory: {subcategory.replace('_', ' ').title()}\n")
                        f.write(f"Index: {image_index}\n")
                        f.write(f"Size: {self.image_width}x{self.image_height}\n")
                        f.write(f"Model: {self.model_id}\n")
                        f.write(f"Prompt: {prompt}\n")
                    return True
                
                # Create a placeholder image
                image = Image.new('RGB', (self.image_width, self.image_height), color='lightgray')
                draw = ImageDraw.Draw(image)
                
                # Add text to show what would be generated
                try:
                    # Try to use a default font
                    font = ImageFont.load_default()
                except:
                    font = None
                
                text_lines = [
                    f"WELLNESS IMAGE PLACEHOLDER",
                    f"Category: {category}",
                    f"Subcategory: {subcategory.replace('_', ' ').title()}",
                    f"Index: {image_index}",
                    f"Size: {self.image_width}x{self.image_height}",
                    "",
                    "This would be generated with:",
                    f"Model: {self.model_id}",
                    "",
                    "Prompt preview:",
                    prompt[:100] + "..." if len(prompt) > 100 else prompt
                ]
                
                y_position = 100
                for line in text_lines:
                    draw.text((50, y_position), line, fill='black', font=font)
                    y_position += 40
                
                image.save(image_path)
            
            # Save prompt file
            self.save_prompt_file(category, subcategory, image_index, prompt)
            
            return True
            
        except Exception as e:
            print(f"    ❌ Error generating {image_filename}: {e}")
            return False
    
    def generate_category_images(self, category: str, subcategories: List[str]) -> Dict:
        """Generate images for all subcategories in a category."""
        print(f"📁 Processing category: {category}")
        print(f"   Subcategories: {', '.join(subcategories)}")
        
        category_results = {}
        
        for subcategory in subcategories:
            print(f"  🎯 Processing: {subcategory}")
            generated_images = []
            
            for i in range(self.images_per_subcategory):
                image_filename = f"{category}_{subcategory}_{i:02d}.png"
                
                if self.image_exists(category, subcategory, i):
                    print(f"    ⏭️  Skipping existing: {image_filename}")
                    self.stats["images_skipped"] += 1
                else:
                    # Create wellness prompt
                    prompt = self.create_wellness_prompt(category, subcategory)
                    
                    # Generate image
                    if self.generate_image(prompt, category, subcategory, i):
                        print(f"    ✓ Generated: {image_filename}")
                        self.stats["images_generated"] += 1
                        generated_images.append(image_filename)
                    else:
                        print(f"    ❌ Failed: {image_filename}")
            
            category_results[subcategory] = generated_images
        
        return category_results
    
    def generate_all_images(self) -> Dict:
        """Generate images for all wellness categories."""
        print("🌟 Starting Comprehensive Wellness Image Generation")
        print("=" * 60)
        print(f"📊 Generation Plan:")
        print(f"   Categories: {self.stats['total_categories']}")
        print(f"   Subcategories: {self.stats['total_subcategories']}")
        print(f"   Total images planned: {self.stats['total_images_planned']}")
        print(f"   Image size: {self.image_width}x{self.image_height} (Paper size compatible)")
        print(f"   Model: {self.model_id}")
        print(f"   Device: {self.device}")
        print()
        
        all_results = {}
        
        for category_idx, (category, subcategories) in enumerate(WELLNESS_CATEGORIES.items(), 1):
            print(f"📂 Category {category_idx}/{len(WELLNESS_CATEGORIES)}: {category}")
            category_results = self.generate_category_images(category, subcategories)
            all_results[category] = category_results
            print()
        
        return all_results
    
    def save_generation_report(self, results: Dict):
        """Save a comprehensive generation report."""
        end_time = datetime.now()
        duration = end_time - self.stats["start_time"]
        
        # Create JSON-serializable stats
        json_stats = self.stats.copy()
        json_stats["start_time"] = self.stats["start_time"].isoformat()
        json_stats["end_time"] = end_time.isoformat()
        json_stats["duration_seconds"] = duration.total_seconds()
        
        report = {
            "generation_info": {
                "timestamp": end_time.isoformat(),
                "duration_seconds": duration.total_seconds(),
                "model_id": self.model_id,
                "device": self.device,
                "seed": self.seed,
                "image_dimensions": [self.image_width, self.image_height],
                "images_per_subcategory": self.images_per_subcategory,
                "paper_size_compatible": f"{self.image_width}x{self.image_height} (US Letter at 300 DPI)"
            },
            "statistics": json_stats,
            "wellness_categories": WELLNESS_CATEGORIES,
            "generation_results": results
        }
        
        report_path = self.output_dir / "generation_report.json"
        with open(report_path, 'w') as f:
            json.dump(report, f, indent=2)
        
        print(f"📋 GENERATION COMPLETE!")
        print("=" * 50)
        print(f"⏱️  Duration: {duration}")
        print(f"📊 Images generated: {self.stats['images_generated']}")
        print(f"⏭️  Images skipped: {self.stats['images_skipped']}")
        print(f"📁 Output directory: {self.output_dir.absolute()}")
        print(f"📄 Report saved: {report_path}")
        print()
        print("🎯 This is what ONE comprehensive script can accomplish!")
        print("✅ All wellness categories processed in a single, unified operation!")

def parse_arguments():
    """Parse command line arguments for easy customization."""
    parser = argparse.ArgumentParser(
        description="Generate wellness and affirmation images using Stable Diffusion",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    
    parser.add_argument('--width', type=int, default=IMAGE_WIDTH,
                        help='Image width in pixels')
    parser.add_argument('--height', type=int, default=IMAGE_HEIGHT,
                        help='Image height in pixels')
    parser.add_argument('--count', type=int, default=IMAGES_PER_SUBCATEGORY,
                        help='Number of images per subcategory')
    parser.add_argument('--output', type=str, default=OUTPUT_BASE_DIR,
                        help='Output directory')
    parser.add_argument('--model', type=str, default=MODEL_ID,
                        help='Stable Diffusion model ID')
    parser.add_argument('--device', type=str, default=DEVICE,
                        help='Device to use (cpu/cuda)')
    parser.add_argument('--seed', type=int, default=DETERMINISTIC_SEED,
                        help='Random seed for reproducibility')
    parser.add_argument('--no-skip-existing', action='store_true',
                        help='Generate images even if they already exist')
    
    # Predefined paper sizes
    parser.add_argument('--paper-size', choices=['letter', 'a4', 'custom'],
                        help='Use predefined paper size (overrides width/height)')
    
    return parser.parse_args()

def main():
    """Main function."""
    print("🌟 Comprehensive Wellness Image Generator")
    print("=" * 60)
    print("This script generates images for ALL wellness categories in ONE unified operation.")
    print("No fragmentation - everything processed together!")
    print()
    
    # Parse command line arguments
    args = parse_arguments()
    
    # Handle paper size presets
    if args.paper_size == 'letter':
        args.width, args.height = 2550, 3300  # US Letter at 300 DPI
        print("📄 Using US Letter paper size (2550x3300 @ 300 DPI)")
    elif args.paper_size == 'a4':
        args.width, args.height = 2480, 3508  # A4 at 300 DPI
        print("📄 Using A4 paper size (2480x3508 @ 300 DPI)")
    
    # Create configuration
    config = {
        'width': args.width,
        'height': args.height,
        'count': args.count,
        'output': args.output,
        'model_id': args.model,
        'device': args.device,
        'seed': args.seed,
        'skip_existing': not args.no_skip_existing
    }
    
    print(f"⚙️  Configuration:")
    for key, value in config.items():
        print(f"   {key}: {value}")
    print()
    
    # Initialize generator
    generator = WellnessImageGenerator(config)
    
    # Generate all images
    results = generator.generate_all_images()
    
    # Save report
    generator.save_generation_report(results)

if __name__ == "__main__":
    main()