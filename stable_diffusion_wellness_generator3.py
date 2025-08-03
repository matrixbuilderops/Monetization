#!/usr/bin/env python3
"""
Stable Diffusion Wellness Image Generator
CPU-compatible image generation for wellness categories
"""

import os
import json
import time
import logging
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Tuple
import argparse

# Set environment variables to disable CUDA/xFormers before importing
os.environ["CUDA_VISIBLE_DEVICES"] = ""
os.environ["FORCE_CPU"] = "1"
os.environ["XFORMERS_DISABLED"] = "1"

try:
    # Disable xFormers to avoid CUDA dependency issues
    os.environ["XFORMERS_MORE_DETAILS"] = "0"
    
    import torch
    # Force PyTorch to use CPU only
    torch.backends.cuda.is_available = lambda: False
    
    from diffusers import StableDiffusionPipeline, DiffusionPipeline
    from PIL import Image
    import numpy as np
    
    print("✅ Successfully imported required packages (CPU mode)")
    
except ImportError as e:
    print(f"❌ Required packages not installed: {e}")
    print("Please install with CPU-only versions:")
    print("pip install torch torchvision --index-url https://download.pytorch.org/whl/cpu")
    print("pip install diffusers pillow numpy transformers accelerate --no-deps")
    print("pip install tokenizers safetensors requests filelock")
    exit(1)
except Exception as e:
    print(f"⚠️  Warning during import: {e}")
    print("Continuing with available functionality...")

class WellnessImageGenerator:
    """Comprehensive wellness image generator using Stable Diffusion"""
    
    # Wellness categories with subcategories
    CATEGORIES = {
        "productivity": ["burnout", "focus", "time_management", "imposter_syndrome"],
        "confidence": ["self-esteem", "public_speaking", "courage"],
        "gratitude": ["daily_gratitude", "thankfulness"],
        "healing": ["emotional", "physical", "spiritual"],
        "focus": ["attention", "clarity", "goals"],
        "creativity": ["inspiration", "flow", "problem_solving"],
        "happiness": ["joy", "contentment", "optimism"],
        "resilience": ["perseverance", "mental_toughness", "bounce_back"],
        "self_love": ["acceptance", "compassion", "affirmation"],
        "stress_relief": ["calm", "relaxation", "letting_go"],
        "abundance": ["wealth", "opportunity", "overflow"],
        "mindfulness": ["present_moment", "awareness", "breathe"],
        "relationships": ["love", "connection", "healing_relationships"],
        "motivation": ["drive", "ambition", "goal_setting"],
        "self_reflection": ["insight", "introspection", "growth"]
    }
    
    # Enhanced prompts for each category
    CATEGORY_PROMPTS = {
        "productivity": {
            "base": "professional, organized workspace, clean aesthetic, minimalist design, productivity tools",
            "burnout": "peaceful recovery scene, rest and restoration, balance, calming colors",
            "focus": "clear mind visualization, concentration symbols, sharp focus imagery",
            "time_management": "clock elements, organized schedule, efficient workflow visualization",
            "imposter_syndrome": "confidence building imagery, authentic self-expression, inner strength"
        },
        "confidence": {
            "base": "empowering imagery, strong posture, bright lighting, uplifting atmosphere",
            "self_esteem": "mirror reflection positivity, self-acceptance symbols, inner glow",
            "public_speaking": "confident presenter, supportive audience, clear communication",
            "courage": "brave symbolism, stepping forward, overcoming obstacles"
        },
        "gratitude": {
            "base": "warm golden lighting, appreciation symbols, thankful gestures, abundance",
            "daily_gratitude": "morning gratitude ritual, journal writing, peaceful reflection",
            "thankfulness": "harvest imagery, giving thanks, community appreciation"
        },
        "healing": {
            "base": "gentle healing energy, soft colors, restoration symbols, peaceful environment",
            "emotional": "heart healing, emotional release, inner peace, comfort",
            "physical": "body wellness, natural remedies, recovery and strength",
            "spiritual": "spiritual awakening, divine connection, enlightenment symbols"
        },
        "focus": {
            "base": "clear vision, concentrated energy, laser focus, mental clarity",
            "attention": "mindful awareness, present moment focus, concentrated effort",
            "clarity": "clear thinking, mental fog lifting, bright understanding",
            "goals": "target achievement, goal visualization, success pathway"
        },
        "creativity": {
            "base": "artistic inspiration, creative flow, vibrant colors, imaginative concepts",
            "inspiration": "lightbulb moments, creative spark, artistic muse",
            "flow": "smooth creative process, effortless creation, artistic flow state",
            "problem_solving": "innovative solutions, creative thinking, breakthrough moments"
        },
        "happiness": {
            "base": "joyful expressions, bright sunshine, cheerful colors, positive energy",
            "joy": "pure happiness, celebration, laughter, blissful moments",
            "contentment": "peaceful satisfaction, inner calm, serene happiness",
            "optimism": "hopeful future, positive outlook, bright possibilities"
        },
        "resilience": {
            "base": "strength symbols, overcoming adversity, steady determination, inner power",
            "perseverance": "continuous effort, never giving up, steady progress",
            "mental_toughness": "strong mindset, emotional strength, unshakeable resolve",
            "bounce_back": "recovery symbols, rising after fall, comeback strength"
        },
        "self_love": {
            "base": "self-care rituals, loving kindness, inner beauty, self-acceptance",
            "acceptance": "embracing imperfections, self-compassion, loving yourself",
            "compassion": "gentle self-treatment, understanding heart, kind gestures",
            "affirmation": "positive self-talk, mirror affirmations, self-encouragement"
        },
        "stress_relief": {
            "base": "calming environment, peaceful scenes, relaxation symbols, tranquil colors",
            "calm": "serene landscape, still water, peaceful meditation",
            "relaxation": "comfort zone, stress melting away, peaceful rest",
            "letting_go": "release symbols, freedom from worry, unburdening"
        },
        "abundance": {
            "base": "prosperity symbols, overflowing goodness, wealth imagery, plenty",
            "wealth": "financial prosperity, golden coins, treasure symbols",
            "opportunity": "open doors, pathways, new possibilities, golden chances",
            "overflow": "cup running over, abundance flowing, plenty for all"
        },
        "mindfulness": {
            "base": "present moment awareness, meditation symbols, peaceful consciousness",
            "present_moment": "here and now focus, mindful awareness, present consciousness",
            "awareness": "heightened consciousness, mindful observation, clear perception",
            "breathe": "breathing exercises, life force, rhythmic breath, oxygen flow"
        },
        "relationships": {
            "base": "connection symbols, heart imagery, loving bonds, relationship harmony",
            "love": "romantic love, universal love, heart connections, loving energy",
            "connection": "human bonds, soul connections, community, togetherness",
            "healing_relationships": "relationship repair, forgiveness, renewed bonds"
        },
        "motivation": {
            "base": "energetic movement, upward arrows, achievement symbols, driving force",
            "drive": "internal motivation, burning desire, passionate pursuit",
            "ambition": "climbing mountains, reaching heights, ambitious goals",
            "goal_setting": "target setting, vision boards, planning success"
        },
        "self_reflection": {
            "base": "mirror imagery, introspective moments, quiet contemplation, inner wisdom",
            "insight": "lightbulb moments, understanding dawning, wisdom revelation",
            "introspection": "looking within, self-examination, inner dialogue",
            "growth": "plant growth, personal evolution, transformation symbols"
        }
    }
    
    def __init__(self, output_dir: str = "wellness_images", model_id: str = "runwayml/stable-diffusion-v1-5"):
        """Initialize the wellness image generator"""
        self.output_dir = Path(output_dir)
        self.model_id = model_id
        self.pipeline = None
        self.default_width = 2550
        self.default_height = 3300
        self.default_images_per_category = 6
        
        # Setup logging
        self.setup_logging()
        
        # Create output directory
        self.output_dir.mkdir(exist_ok=True)
        
    def setup_logging(self):
        """Setup logging configuration"""
        log_file = self.output_dir / "generation_log.txt"
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(log_file),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)
        
    def initialize_pipeline(self):
        """Initialize the Stable Diffusion pipeline for CPU"""
        print("🚀 Initializing Stable Diffusion pipeline (CPU mode)...")
        print("⚠️  Note: CPU generation will be slower than GPU. Please be patient.")
        
        try:
            # Force CPU usage and disable problematic features
            device = "cpu"
            torch_dtype = torch.float32
            
            # Disable all CUDA-related optimizations
            torch.backends.cudnn.enabled = False
            
            print("📦 Loading model (this may take a few minutes)...")
            
            # Load with CPU-safe parameters
            self.pipeline = StableDiffusionPipeline.from_pretrained(
                self.model_id,
                torch_dtype=torch_dtype,
                use_safetensors=True,
                safety_checker=None,
                requires_safety_checker=False,
                local_files_only=False,
                variant="fp16" if torch_dtype == torch.float16 else None
            )
            
            # Move to CPU and apply CPU optimizations
            print("⚙️  Configuring for CPU inference...")
            self.pipeline = self.pipeline.to(device)
            
            # Enable memory-efficient attention slicing for CPU
            self.pipeline.enable_attention_slicing(1)
            
            # Enable CPU offload if available
            try:
                self.pipeline.enable_sequential_cpu_offload()
                print("✅ CPU offload enabled")
            except:
                print("⚠️  CPU offload not available, continuing...")
            
            # Disable xformers to avoid CUDA issues
            try:
                self.pipeline.disable_xformers_memory_efficient_attention()
                print("✅ xFormers disabled successfully")
            except:
                print("⚠️  Could not disable xFormers, continuing...")
            
            print("✅ Pipeline initialized successfully!")
            self.logger.info(f"Pipeline initialized with model: {self.model_id}")
            
        except Exception as e:
            print(f"❌ Error initializing pipeline: {e}")
            print("💡 Troubleshooting suggestions:")
            print("   1. Try: pip uninstall xformers")
            print("   2. Reinstall PyTorch CPU: pip install torch torchvision --index-url https://download.pytorch.org/whl/cpu")
            print("   3. Use a smaller model like 'CompVis/stable-diffusion-v1-4'")
            self.logger.error(f"Pipeline initialization failed: {e}")
            raise
            
    def create_category_folders(self, categories: List[str]):
        """Create folder structure for selected categories"""
        created_folders = []
        
        for category in categories:
            category_path = self.output_dir / category
            category_path.mkdir(exist_ok=True)
            created_folders.append(category_path)
            
            # Create subcategory folders
            for subcategory in self.CATEGORIES[category]:
                subcategory_path = category_path / subcategory
                subcategory_path.mkdir(exist_ok=True)
                created_folders.append(subcategory_path)
                
        self.logger.info(f"Created {len(created_folders)} folders")
        return created_folders
        
    def generate_enhanced_prompt(self, category: str, subcategory: str, image_num: int) -> str:
        """Generate enhanced prompt for specific category and subcategory"""
        base_prompt = self.CATEGORY_PROMPTS[category]["base"]
        specific_prompt = self.CATEGORY_PROMPTS[category].get(subcategory, subcategory.replace("_", " "))
        
        # Style enhancements
        style_additions = [
            "high quality, detailed, professional photography",
            "beautiful lighting, aesthetic composition",
            "8k resolution, sharp focus, vibrant colors",
            "inspirational, uplifting, positive energy"
        ]
        
        # Combine prompts
        full_prompt = f"{specific_prompt}, {base_prompt}, {', '.join(style_additions)}"
        
        # Add variety with image number
        if image_num % 3 == 0:
            full_prompt += ", artistic illustration style"
        elif image_num % 3 == 1:
            full_prompt += ", photorealistic style"
        else:
            full_prompt += ", minimalist design"
            
        return full_prompt
        
    def generate_image(self, prompt: str, width: int, height: int, num_inference_steps: int = 15) -> Optional[Image.Image]:
        """Generate a single image using the pipeline"""
        try:
            # CPU-optimized generation settings
            with torch.no_grad():  # Reduce memory usage
                image = self.pipeline(
                    prompt=prompt,
                    width=width,
                    height=height,
                    num_inference_steps=num_inference_steps,
                    guidance_scale=7.5,
                    generator=torch.Generator().manual_seed(int(time.time())),
                    # CPU-specific optimizations
                    enable_vae_slicing=True,
                    enable_vae_tiling=True if hasattr(self.pipeline, 'enable_vae_tiling') else False
                ).images[0]
            
            return image
            
        except Exception as e:
            self.logger.error(f"Error generating image: {e}")
            print(f"⚠️  Generation failed: {e}")
            
            # Try with reduced settings
            try:
                print("🔄 Retrying with reduced settings...")
                with torch.no_grad():
                    image = self.pipeline(
                        prompt=prompt,
                        width=min(width, 512),  # Reduce size for CPU
                        height=min(height, 512),
                        num_inference_steps=10,  # Fewer steps
                        guidance_scale=7.0
                    ).images[0]
                
                # Resize back to original dimensions if needed
                if width > 512 or height > 512:
                    image = image.resize((width, height), Image.Resampling.LANCZOS)
                
                return image
                
            except Exception as e2:
                self.logger.error(f"Retry also failed: {e2}")
                return None
            
    def save_image_with_metadata(self, image: Image.Image, filepath: Path, prompt: str, category: str, subcategory: str):
        """Save image with metadata"""
        # Save image
        image.save(filepath, "PNG", quality=95, optimize=True)
        
        # Save metadata
        metadata = {
            "timestamp": datetime.now().isoformat(),
            "prompt": prompt,
            "category": category,
            "subcategory": subcategory,
            "dimensions": f"{image.width}x{image.height}",
            "model": self.model_id
        }
        
        metadata_file = filepath.with_suffix('.json')
        with open(metadata_file, 'w') as f:
            json.dump(metadata, f, indent=2)
            
    def generate_category_images(self, category: str, num_images: int, width: int, height: int) -> int:
        """Generate images for a specific category"""
        print(f"\n🎨 Generating images for category: {category.upper()}")
        generated_count = 0
        
        for subcategory in self.CATEGORIES[category]:
            print(f"  📁 Subcategory: {subcategory}")
            subcategory_path = self.output_dir / category / subcategory
            
            for i in range(num_images):
                print(f"    🖼️  Generating image {i+1}/{num_images}...", end=" ")
                
                # Generate enhanced prompt
                prompt = self.generate_enhanced_prompt(category, subcategory, i)
                
                # Generate image
                start_time = time.time()
                image = self.generate_image(prompt, width, height)
                generation_time = time.time() - start_time
                
                if image:
                    # Save image with timestamp
                    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                    filename = f"{subcategory}_{i+1:02d}_{timestamp}.png"
                    filepath = subcategory_path / filename
                    
                    self.save_image_with_metadata(image, filepath, prompt, category, subcategory)
                    
                    print(f"✅ Saved ({generation_time:.1f}s)")
                    generated_count += 1
                    
                    self.logger.info(f"Generated: {filepath}")
                else:
                    print("❌ Failed")
                    
        return generated_count
        
    def display_menu(self):
        """Display interactive menu"""
        print("\n" + "="*60)
        print("🌟 WELLNESS IMAGE GENERATOR - STABLE DIFFUSION 🌟")
        print("="*60)
        print("\nAvailable Categories:")
        
        for i, (category, subcategories) in enumerate(self.CATEGORIES.items(), 1):
            print(f"{i:2d}. {category.upper():<15} ({len(subcategories)} subcategories)")
            
        print(f"\n{len(self.CATEGORIES)+1:2d}. ALL CATEGORIES")
        print(f"{len(self.CATEGORIES)+2:2d}. CUSTOM SELECTION")
        print(f"{len(self.CATEGORIES)+3:2d}. SETTINGS")
        print(f"{len(self.CATEGORIES)+4:2d}. EXIT")
        
    def get_user_selection(self) -> Tuple[List[str], int, int, int]:
        """Get user selection from menu"""
        while True:
            self.display_menu()
            
            try:
                choice = input(f"\nEnter your choice (1-{len(self.CATEGORIES)+4}): ").strip()
                
                if choice == str(len(self.CATEGORIES)+4):  # EXIT
                    return [], 0, 0, 0
                    
                elif choice == str(len(self.CATEGORIES)+3):  # SETTINGS
                    return self.configure_settings()
                    
                elif choice == str(len(self.CATEGORIES)+1):  # ALL CATEGORIES
                    categories = list(self.CATEGORIES.keys())
                    num_images = self.get_image_count()
                    return categories, num_images, self.default_width, self.default_height
                    
                elif choice == str(len(self.CATEGORIES)+2):  # CUSTOM SELECTION
                    return self.get_custom_selection()
                    
                else:
                    choice_idx = int(choice) - 1
                    if 0 <= choice_idx < len(self.CATEGORIES):
                        category = list(self.CATEGORIES.keys())[choice_idx]
                        num_images = self.get_image_count()
                        return [category], num_images, self.default_width, self.default_height
                    else:
                        print("❌ Invalid choice. Please try again.")
                        
            except (ValueError, IndexError):
                print("❌ Invalid input. Please enter a number.")
                
    def get_custom_selection(self) -> Tuple[List[str], int, int, int]:
        """Get custom category selection"""
        print("\n📋 CUSTOM CATEGORY SELECTION")
        print("Enter category numbers separated by commas (e.g., 1,3,5):")
        
        category_list = list(self.CATEGORIES.keys())
        for i, category in enumerate(category_list, 1):
            print(f"{i:2d}. {category}")
            
        try:
            selections = input("\nYour selection: ").strip().split(',')
            selected_categories = []
            
            for sel in selections:
                idx = int(sel.strip()) - 1
                if 0 <= idx < len(category_list):
                    selected_categories.append(category_list[idx])
                    
            if selected_categories:
                num_images = self.get_image_count()
                return selected_categories, num_images, self.default_width, self.default_height
            else:
                print("❌ No valid categories selected.")
                return self.get_user_selection()
                
        except ValueError:
            print("❌ Invalid input format.")
            return self.get_user_selection()
            
    def get_image_count(self) -> int:
        """Get number of images per category from user"""
        while True:
            try:
                count = input(f"\nImages per category (default {self.default_images_per_category}): ").strip()
                if not count:
                    return self.default_images_per_category
                    
                count = int(count)
                if count > 0:
                    return count
                else:
                    print("❌ Please enter a positive number.")
                    
            except ValueError:
                print("❌ Please enter a valid number.")
                
    def configure_settings(self) -> Tuple[List[str], int, int, int]:
        """Configure generation settings"""
        print("\n⚙️  SETTINGS CONFIGURATION")
        print(f"Current settings:")
        print(f"  📐 Image dimensions: {self.default_width}x{self.default_height}")
        print(f"  🖼️  Images per category: {self.default_images_per_category}")
        print(f"  📁 Output directory: {self.output_dir}")
        
        # Image dimensions
        change_dims = input("\nChange image dimensions? (y/n): ").strip().lower()
        if change_dims == 'y':
            try:
                width = int(input(f"Width (current {self.default_width}): ") or self.default_width)
                height = int(input(f"Height (current {self.default_height}): ") or self.default_height)
                self.default_width = width
                self.default_height = height
                print(f"✅ Dimensions updated to {width}x{height}")
            except ValueError:
                print("❌ Invalid dimensions. Keeping current settings.")
                
        # Images per category
        change_count = input("Change default images per category? (y/n): ").strip().lower()
        if change_count == 'y':
            try:
                count = int(input(f"Images per category (current {self.default_images_per_category}): ") or self.default_images_per_category)
                if count > 0:
                    self.default_images_per_category = count
                    print(f"✅ Default image count updated to {count}")
            except ValueError:
                print("❌ Invalid count. Keeping current settings.")
                
        # Return to main menu
        input("\nPress Enter to return to main menu...")
        return self.get_user_selection()
        
    def generate_wellness_images(self):
        """Main generation workflow"""
        print("🌟 Welcome to the Wellness Image Generator!")
        
        # Initialize pipeline
        if not self.pipeline:
            self.initialize_pipeline()
            
        while True:
            # Get user selection
            categories, num_images, width, height = self.get_user_selection()
            
            if not categories:  # Exit selected
                print("\n👋 Thank you for using the Wellness Image Generator!")
                break
                
            # Create folders
            print(f"\n📁 Creating folder structure...")
            self.create_category_folders(categories)
            
            # Generate images
            total_generated = 0
            start_time = time.time()
            
            print(f"\n🎨 Starting generation for {len(categories)} categories...")
            print(f"📊 Settings: {num_images} images per category, {width}x{height} pixels")
            
            for category in categories:
                category_count = self.generate_category_images(category, num_images, width, height)
                total_generated += category_count
                
            # Summary
            total_time = time.time() - start_time
            print(f"\n✅ Generation Complete!")
            print(f"📊 Total images generated: {total_generated}")
            print(f"⏱️  Total time: {total_time/60:.1f} minutes")
            print(f"📁 Images saved to: {self.output_dir}")
            
            # Continue or exit
            continue_gen = input("\nGenerate more images? (y/n): ").strip().lower()
            if continue_gen != 'y':
                print("\n👋 Thank you for using the Wellness Image Generator!")
                break

def install_cpu_dependencies():
    """Helper function to install CPU-compatible dependencies"""
    print("🔧 CPU-Compatible Installation Instructions:")
    print("=" * 50)
    print("1. Uninstall problematic packages:")
    print("   pip uninstall xformers -y")
    print("   pip uninstall torch torchvision -y")
    print()
    print("2. Install CPU-only PyTorch:")
    print("   pip install torch torchvision --index-url https://download.pytorch.org/whl/cpu")
    print()
    print("3. Install other dependencies:")
    print("   pip install diffusers pillow numpy transformers accelerate")
    print("   pip install tokenizers safetensors requests filelock")
    print()
    print("4. If you still get xFormers errors, try:")
    print("   export XFORMERS_DISABLED=1")
    print("   export FORCE_CPU=1")
    print()

def main():
    """Main function"""
    parser = argparse.ArgumentParser(description="Wellness Image Generator using Stable Diffusion")
    parser.add_argument("--output-dir", default="wellness_images", help="Output directory for images")
    parser.add_argument("--model", default="runwayml/stable-diffusion-v1-5", help="Stable Diffusion model ID")
    parser.add_argument("--batch", action="store_true", help="Run in batch mode (generate all categories)")
    parser.add_argument("--images-per-category", type=int, default=6, help="Number of images per category")
    parser.add_argument("--width", type=int, default=2550, help="Image width")
    parser.add_argument("--height", type=int, default=3300, help="Image height")
    parser.add_argument("--install-help", action="store_true", help="Show installation instructions")
    
    args = parser.parse_args()
    
    if args.install_help:
        install_cpu_dependencies()
        return
    
    # Create generator instance
    generator = WellnessImageGenerator(
        output_dir=args.output_dir,
        model_id=args.model
    )
    
    # Set custom defaults if provided
    if args.images_per_category != 6:
        generator.default_images_per_category = args.images_per_category
    if args.width != 2550:
        generator.default_width = args.width
    if args.height != 3300:
        generator.default_height = args.height
    
    try:
        if args.batch:
            # Batch mode - generate all categories
            print("🚀 Running in batch mode - generating all categories")
            generator.initialize_pipeline()
            generator.create_category_folders(list(generator.CATEGORIES.keys()))
            
            total_generated = 0
            start_time = time.time()
            
            for category in generator.CATEGORIES.keys():
                count = generator.generate_category_images(
                    category, 
                    args.images_per_category, 
                    args.width, 
                    args.height
                )
                total_generated += count
                
            total_time = time.time() - start_time
            print(f"\n✅ Batch generation complete!")
            print(f"📊 Total images: {total_generated}")
            print(f"⏱️  Total time: {total_time/60:.1f} minutes")
            
        else:
            # Interactive mode
            generator.generate_wellness_images()
            
    except KeyboardInterrupt:
        print("\n\n⚠️  Generation interrupted by user.")
    except Exception as e:
        print(f"\n❌ An error occurred: {e}")
        print("\n💡 If you're getting CUDA/xFormers errors, try:")
        print("   python stable_diffusion_wellness_generator.py --install-help")
        logging.error(f"Fatal error: {e}", exc_info=True)

if __name__ == "__main__":
    main()
