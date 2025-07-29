import random
import os
import json
from datetime import datetime
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

# === Configuration ===
CATEGORIES = [
    "productivity",
    "self-worth",
    "anxiety",
    "resilience",
    "positivity",
    "healing",
    "confidence",
    "relationships",
    "gratitude",
    "focus",
    "career",
    "depression",
    "energy",
    "calm",
    "discipline"
]

OUTPUT_DIR = Path("model_output")
IMAGE_FONT = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"

# === Helpers ===
def generate_affirmation(category: str) -> str:
    return f"[{category.upper()}] You are in control of your {category} and capable of overcoming challenges."

def save_text(affirmation: str, path: Path):
    with open(path, "w") as f:
        f.write(affirmation)

def save_pdf(affirmation: str, path: Path):
    c = canvas.Canvas(str(path), pagesize=letter)
    width, height = letter
    c.setFont("Helvetica", 20)
    c.drawString(100, height - 100, affirmation)
    c.save()

def save_image(affirmation: str, path: Path):
    img = Image.new("RGB", (800, 400), color=(255, 255, 255))
    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype(IMAGE_FONT, 24)
    draw.text((50, 180), affirmation, font=font, fill=(0, 0, 0))
    img.save(path)

# === Main Generation ===
def generate_pack():
    OUTPUT_DIR.mkdir(exist_ok=True)
    now = datetime.now().strftime("%Y%m%d_%H%M%S")
    pack_dir = OUTPUT_DIR / f"affirmations_{now}"
    pack_dir.mkdir()

    log = {"generated": []}

    category = random.choice(CATEGORIES)
    count = random.randint(3, 7)

    for i in range(count):
        affirmation = generate_affirmation(category)
        base_filename = f"{category}_{i}"
        
        # Save formats
        save_text(affirmation, pack_dir / f"{base_filename}.txt")
        save_pdf(affirmation, pack_dir / f"{base_filename}.pdf")
        save_image(affirmation, pack_dir / f"{base_filename}.png")

        log["generated"].append({
            "category": category,
            "affirmation": affirmation,
            "files": [
                f"{base_filename}.txt",
                f"{base_filename}.pdf",
                f"{base_filename}.png"
            ]
        })

    # Save log
    with open(pack_dir / "generation_log.json", "w") as f:
        json.dump(log, f, indent=2)

if __name__ == "__main__":
    generate_pack()
