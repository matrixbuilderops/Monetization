import os
import json
import random
from datetime import datetime
from utils import create_image_from_text, create_pdf_from_text

# Categories and subcategories
CATEGORIES = {
    "productivity": ["focus", "motivation", "time management"],
    "work": ["burnout", "imposter syndrome", "deadlines"],
    "relationships": ["toxic family", "breakups", "self-worth"],
    "self-esteem": ["confidence", "inner peace", "self-acceptance"],
    "mental_health": ["anxiety", "depression", "stress"],
    "healing": ["grief", "recovery", "letting go"],
    "body": ["appearance", "fitness", "health"],
    "money": ["abundance", "savings", "debt"],
    "sleep": ["relaxation", "insomnia", "winding down"],
    "spirituality": ["purpose", "gratitude", "presence"],
    "addiction": ["sobriety", "resilience", "self-control"],
    "career": ["success", "promotion", "goal-setting"],
    "parenting": ["patience", "balance", "love"],
    "identity": ["acceptance", "expression", "empowerment"],
    "stress_relief": ["calm", "clarity", "unwind"]
}

NUM_AFFIRMATIONS = random.randint(3, 6)
CATEGORY = random.choice(list(CATEGORIES.keys()))
SUBCATEGORY = random.choice(CATEGORIES[CATEGORY])

# Generate directory structure
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
base_path = f"model_output/{timestamp}_{CATEGORY}_{SUBCATEGORY}"
os.makedirs(base_path, exist_ok=True)

# Simulated LLM output (replace this block with actual LLM call)
affirmations = [
    f"{i+1}. You are strong and capable of overcoming any {SUBCATEGORY} challenges."
    for i in range(NUM_AFFIRMATIONS)
]

# Save each in all formats
for i, affirmation in enumerate(affirmations):
    sku = f"{CATEGORY[:3]}-{SUBCATEGORY[:3]}-{timestamp}-{i+1}"
    
    txt_path = os.path.join(base_path, f"{sku}.txt")
    pdf_path = os.path.join(base_path, f"{sku}.pdf")
    img_path = os.path.join(base_path, f"{sku}.png")
    json_path = os.path.join(base_path, f"{sku}.json")

    with open(txt_path, "w") as f:
        f.write(affirmation)

    create_pdf_from_text(affirmation, pdf_path)
    create_image_from_text(affirmation, img_path)

    with open(json_path, "w") as f:
        json.dump({
            "sku": sku,
            "category": CATEGORY,
            "subcategory": SUBCATEGORY,
            "text": affirmation
        }, f, indent=2)

# Final log
print(f"Generated {NUM_AFFIRMATIONS} affirmations in {base_path}")
