import os
import random
from PIL import Image
import numpy as np
import torch
from diffusers import StableDiffusionPipeline
# User-configurable parameters
IMAGE_WIDTH = 2550
IMAGE_HEIGHT = 3300
IMAGES_PER_SUB CATEGORY = 6
OUTPUT_DIR = "stable_diffusion_images"
MODEL_ID = "runwayml/stable-diffusion-v1-5"
DETERMINISTIC_SEED = 42
# Create output directory if it doesn't exist
os.makedirs(OUTPUT_DIR, exist_ok=True)
    # Generate filename using subcategory and deterministic seed
    file_name = f"{subcategory}_{DETERMINISTIC_SEED}.png"
    image_path = os.path.join(OUTPUT_DIR, subcategory, file_name)
    # Skip generation if image already exists
        print(f"Image '{file_name}' already exists. Skipping generation.")
        return
    # Create subdirectory for subcategory if it doesn't exist
    subcategory_dir = os.path.join(OUTPUT_DIR, subcategory)
    os.makedirs(subcategory_dir, exist_ok=True)
    # Initialize pipeline with CPU-compatible setup
    pipe = StableDiffusionPipeline.from_pretrained(MODEL_ID, use_cpu=True).to("cpu")
    # Generate image
    print(f"Generating '{file_name}'...")
    image = pipe(subcategory, num_images_per_prompt=IMAGES_PER_SUB_CATEGORY, height=IMAGE_HEIGHT, width=IMAGE_WIDTH)[0]["images"][0]
    # Save image
    image.save(image_path)
    print(f"Saved '{file_name}' to {subcategory_dir}.")
    random.seed(DETERMINISTIC_SEED)
    np.random.seed(DETERMINISTIC_SEED)
    torch.manual_seed(DETERMINISTIC_SEED)
    # Example subcategory
    subcategory = "example_subcategory"
    generate_image(subcategory)