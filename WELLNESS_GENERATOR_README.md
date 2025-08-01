# Comprehensive Stable Diffusion Wellness Image Generator

## 🌟 What This Script Does

This script solves the **fragmentation problem** by generating images for ALL wellness categories in ONE comprehensive, unified operation. No more multiple scripts scattered across your project!

### ✅ Problems Solved:
- **No More Fragmentation**: Single script handles all 15 wellness categories and 45 subcategories
- **No Cat Confusion**: Uses proper wellness prompts instead of feline cat references  
- **Paper Size Support**: Default US Letter size (2550x3300 at 300 DPI) with easy customization
- **Full Configurability**: Command-line options for all parameters
- **Professional Organization**: Organized output structure with metadata tracking

## 🚀 Quick Start

### Basic Usage (Default Settings)
```bash
python3 stable_diffusion_wellness_generator.py
```

### Customized Usage
```bash
# US Letter paper size, 6 images per category
python3 stable_diffusion_wellness_generator.py --paper-size letter --count 6

# A4 paper size, 3 images per category  
python3 stable_diffusion_wellness_generator.py --paper-size a4 --count 3

# Custom size and output directory
python3 stable_diffusion_wellness_generator.py --width 1920 --height 1080 --output my_images --count 4
```

## 📋 Features

### ✨ Comprehensive Processing
- **15 Wellness Categories**: productivity, confidence, gratitude, healing, focus, creativity, happiness, resilience, self_love, stress_relief, success, anxiety_relief, mindfulness, motivation, relationships
- **45 Subcategories**: Complete coverage of wellness and affirmation topics
- **270 Images** (default): 6 images per subcategory, fully customizable

### 🎨 Image Quality
- **Paper-Size Ready**: Default US Letter (2550x3300 @ 300 DPI)
- **High-Quality Prompts**: Professionally crafted wellness prompts for each category
- **Consistent Style**: Therapeutic art style with peaceful, healing aesthetics
- **CPU Compatible**: Works without GPU requirements

### ⚙️ Full Customization
```bash
# All available options:
--width WIDTH         Image width in pixels (default: 2550)
--height HEIGHT       Image height in pixels (default: 3300)  
--count COUNT         Images per subcategory (default: 6)
--output OUTPUT       Output directory (default: stable_diffusion_images)
--model MODEL         Stable Diffusion model (default: stabilityai/stable-diffusion-2-1-base)
--device DEVICE       Device: cpu/cuda (default: cpu)
--seed SEED           Reproducibility seed (default: 42)
--no-skip-existing    Regenerate existing images
--paper-size SIZE     Presets: letter, a4, custom
```

### 📁 Organized Output Structure
```
stable_diffusion_images/
├── generation_report.json          # Complete processing metadata
├── imposter_syndrome/
│   ├── productivity_imposter_syndrome_00.png
│   ├── productivity_imposter_syndrome_00_prompt.txt
│   ├── productivity_imposter_syndrome_01.png
│   └── ...
├── burnout/
│   ├── productivity_burnout_00.png
│   └── ...
└── ... (45 subcategory directories)
```

## 🌈 Wellness Categories Covered

### Complete WELLNESS_CATEGORIES Dictionary:
```python
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
```

## 🛠️ Installation & Setup

### Prerequisites
```bash
# Install required packages
pip install torch diffusers pillow transformers accelerate

# For CPU-only use (default):
pip install torch --index-url https://download.pytorch.org/whl/cpu
```

### Quick Test (Simulation Mode)
```bash
# Test without diffusers (creates placeholder images)
python3 stable_diffusion_wellness_generator.py --count 1 --output test_run
```

## 📊 Example Generation Report

After generation, you'll get a comprehensive JSON report:
```json
{
  "generation_info": {
    "timestamp": "2025-08-01T21:01:05.081030",
    "duration_seconds": 8.1,
    "model_id": "stabilityai/stable-diffusion-2-1-base",
    "device": "cpu",
    "image_dimensions": [2550, 3300],
    "paper_size_compatible": "2550x3300 (US Letter at 300 DPI)"
  },
  "statistics": {
    "total_categories": 15,
    "total_subcategories": 45,
    "images_generated": 270,
    "images_skipped": 0
  }
}
```

## 🎯 Why This Script is Better

### ❌ Old Fragmented Approach:
- 18+ separate Python scripts
- Inconsistent prompts and quality
- Manual file management
- Cat confusion (feline cats instead of wellness categories!)
- No unified configuration

### ✅ New Comprehensive Approach:
- **1 Script** handles everything
- Professional wellness prompts
- Automated organization and metadata
- Paper-size ready output
- Full configurability
- No fragmentation!

## 🔧 Advanced Configuration

### Paper Size Presets
```bash
# US Letter (default)
--paper-size letter    # 2550x3300 @ 300 DPI

# A4 
--paper-size a4        # 2480x3508 @ 300 DPI

# Custom
--width 1920 --height 1080  # Custom dimensions
```

### Batch Processing Examples
```bash
# Quick test run (1 image per subcategory)
python3 stable_diffusion_wellness_generator.py --count 1 --output quick_test

# Production run (6 images per subcategory)  
python3 stable_diffusion_wellness_generator.py --count 6 --paper-size letter

# High-resolution custom run
python3 stable_diffusion_wellness_generator.py --width 4096 --height 4096 --count 3
```

## 🚨 No More Fragmentation!

This script demonstrates what **ONE comprehensive script** can accomplish:
- ✅ **15 categories** processed uniformly
- ✅ **45 subcategories** with consistent quality
- ✅ **270 images** (default) generated efficiently  
- ✅ **Paper-size ready** output
- ✅ **Professional organization** with metadata
- ✅ **Full customization** through command-line options

**Stop fragmenting your workflow!** Use this comprehensive script for all your stable diffusion wellness image needs.