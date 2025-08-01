import os
import random
from typing import Dict, List, Tuple

import torch
from diffusers import DiffusionPipeline
from PIL import Image

# Set seeds for reproducibility
torch.manual_seed(42)
random.seed(42)

# Define the CATS dictionary
CATS = {
    "persian": ["black", "gray", "white"],
    "siamese": ["pointed", "seal-point", "blue-point"],
    "maine_coon": ["ginger", "silver", "tabby"],
}

# Define a function to generate images for a given subcategory
def generate_images(subcategory: str, variations: List[str]) -> None:
    # Load the diffusers pipeline with the stabilityai/stable-diffusion-2-1-base model
    pipe = DiffusionPipeline.from_pretrained("stabilityai/stable-diffusion-2-1-base")
    pipe = pipe.to("cuda")

    # Generate six images for each variation
    for variation in variations:
        print(f"Generating images for {subcategory} - {variation}...")
        
        # Create a directory to save the generated images
        os.makedirs(f"{subcategory}_{variation}", exist_ok=True)

        for i in range(6):
            # Generate an image
            image = pipe([f"A {subcategory} cat with {variation} fur"], height=512, width=512).images[0]

            # Save the generated image
            image.save(f"{subcategory}_{variation}/generated_image_{i}.png")

# Generate images for each subcategory and variation in the CATS dictionary
for subcategory, variations in CATS.items():
    generate_images(subcategory, variations)