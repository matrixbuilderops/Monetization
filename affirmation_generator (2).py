import os
import json
import random
import datetime
from utils.text_to_image import text_to_image
from utils.text_to_pdf import text_to_pdf
from bridge import query_model  # Assumes local model query bridge

# Affirmation categories
CATEGORIES = [
    "self-esteem", "productivity", "stress relief", "gratitude", "healing",
    "confidence", "mindfulness", "abundance", "motivation", "purpose",
    "relationships", "forgiveness", "career", "focus", "resilience"
]

# Parameters
N = random.randint(4, 6)  # Random number of affirmations to generate
output_dir = "model_output"
os.makedirs(output_dir, exist_ok=True)

# Generate affirmations
affirmations = []
for i in range(N):
    category = random.choice(CATEGORIES)
    prompt = f"Write one {category} affirmation."
    response = query_model(prompt).strip()
    affirmations.append({"category": category, "affirmation": response})

    # Timestamp for unique file naming
    ts = datetime.datetime.now().strftime("%Y%m%d%H%M%S%f")
    base_path = os.path.join(output_dir, f"affirmation_{i+1}_{ts}")

    # Save .txt
    with open(f"{base_path}.txt", "w") as f:
        f.write(response)

    # Save .pdf
    text_to_pdf(response, f"{base_path}.pdf")

    # Save .png
    text_to_image(response, f"{base_path}.png")

# Save metadata
with open(os.path.join(output_dir, "generation_log.json"), "w") as f:
    json.dump(affirmations, f, indent=2)

print(f"Generated {len(affirmations)} affirmations.")
