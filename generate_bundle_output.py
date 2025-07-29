import os
import shutil
import random
import json
from datetime import datetime
from utils.generator import generate_affirmation_set  # Model interaction
from utils.formatters import save_as_text, save_as_pdf, save_as_image  # Output converters

# Affirmation categories
CATEGORIES = [
    "productivity", "confidence", "gratitude", "healing", "focus",
    "creativity", "happiness", "resilience", "self_love", "stress_relief",
    "success", "anxiety_relief", "mindfulness", "motivation", "relationships"
]

# Output paths
MODEL_OUTPUT = "model_output"
READY_UPLOAD = ["ready_for_upload/etsy", "ready_for_upload/gumtree"]

# Generate unique ID
def unique_id():
    return f"{random.randint(0, 99999):05d}"

# Create bundle directory
def make_bundle_dir(category: str, uid: str) -> str:
    path = os.path.join(MODEL_OUTPUT, f"{category}_{uid}")
    os.makedirs(path, exist_ok=True)
    return path

# Move to upload folders
def move_to_ready(path: str):
    for platform_path in READY_UPLOAD:
        dest = os.path.join(platform_path, os.path.basename(path))
        shutil.copytree(path, dest)
    shutil.rmtree(path)

# Main process
def generate_bundle():
    category = random.choice(CATEGORIES)
    uid = unique_id()
    path = make_bundle_dir(category, uid)
    
    count = random.randint(3, 7)
    affirmations = generate_affirmation_set(category, count)
    metadata = {"category": category, "affirmations": []}

    for idx, text in enumerate(affirmations, 1):
        file_id = f"{idx:03d}"
        save_as_text(path, text, file_id)
        save_as_pdf(path, text, file_id)
        save_as_image(path, text, file_id)
        metadata["affirmations"].append({"id": file_id, "text": text})

    # Save metadata
    with open(os.path.join(path, "metadata.json"), "w") as meta_file:
        json.dump(metadata, meta_file, indent=2)

    move_to_ready(path)

if __name__ == "__main__":
    generate_bundle()
