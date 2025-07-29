import os
import sys
import json
import random
import argparse
from datetime import datetime
from PIL import Image, ImageDraw, ImageFont
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
import subprocess

FONT_PATH = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
OUTPUT_ROOT = "ready_for_upload/etsy"
BACKGROUND_IMAGE_PATH = "background.jpg"
OLLAMA_MODEL = "mixtral:8x7b-instruct-v0.1-q6_K"

# Full category/subcategory map
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

def ensure_dir(path):
    os.makedirs(path, exist_ok=True)

def call_model(prompt: str) -> str:
    try:
        result = subprocess.run(
            ["ollama", "run", OLLAMA_MODEL],
            input=prompt,
            text=True,
            capture_output=True,
            timeout=30
        )
        if result.returncode != 0:
            raise RuntimeError(result.stderr.strip())
        return result.stdout.strip() or "Default fallback affirmation."
    except Exception as e:
        return f"Model failed: {str(e)}"

def generate_background_image(text: str, output_path: str):
    if os.path.exists(BACKGROUND_IMAGE_PATH):
        bg = Image.open(BACKGROUND_IMAGE_PATH).convert("RGB").resize((800, 400))
    else:
        bg = Image.new("RGB", (800, 400), color=(245, 245, 245))
    draw = ImageDraw.Draw(bg)
    font = ImageFont.truetype(FONT_PATH, 24)
    text_box = draw.textbbox((0, 0), text, font=font)
    x = (bg.width - text_box[2]) // 2
    y = (bg.height - text_box[3]) // 2
    draw.text((x, y), text, fill=(0, 0, 0), font=font)
    bg.save(output_path)

def generate_pdf(text: str, output_path: str):
    c = canvas.Canvas(output_path, pagesize=letter)
    width, height = letter
    if os.path.exists(BACKGROUND_IMAGE_PATH):
        c.drawImage(ImageReader(BACKGROUND_IMAGE_PATH), 0, 0, width=width, height=height)
    c.setFont("Helvetica-Bold", 14)
    text_object = c.beginText(72, height - 100)
    for line in text.split("\n"):
        text_object.textLine(line)
    c.drawText(text_object)
    c.save()

def save_text_file(text: str, output_path: str):
    with open(output_path, "w") as f:
        f.write(text)

def generate_affirmation_files(text: str, basename: str, output_dir: str):
    save_text_file(text, os.path.join(output_dir, f"{basename}.txt"))
    generate_background_image(text, os.path.join(output_dir, f"{basename}.png"))
    generate_pdf(text, os.path.join(output_dir, f"{basename}.pdf"))

def main(category: str, subcategory: str, count: int):
    if category not in CATEGORIES or subcategory not in CATEGORIES[category]:
        print(f"Invalid category or subcategory: {category}/{subcategory}")
        sys.exit(1)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    bundle_dir = os.path.join(OUTPUT_ROOT, f"{subcategory}_{category}_{timestamp}")
    ensure_dir(bundle_dir)

    for i in range(count):
        prompt = f"Generate a {subcategory} affirmation for {category}."
        text = call_model(prompt)
        index = f"{i+1:03}"
        generate_affirmation_files(text, f"{index}_{subcategory}_affirmation", bundle_dir)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--category", required=True)
    parser.add_argument("--subcategory", required=True)
    parser.add_argument("--count", type=int, default=7)
    args = parser.parse_args()
    main(args.category, args.subcategory, args.count)
