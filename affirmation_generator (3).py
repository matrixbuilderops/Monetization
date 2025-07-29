import os
import json
from datetime import datetime
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

# Constants
FONT_PATH = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
OUTPUT_DIR = Path("model_output")
LOG_FILE = OUTPUT_DIR / "bridge_log.txt"
BATCH_SIZE = 5

# Ensure output directory exists
OUTPUT_DIR.mkdir(exist_ok=True)

# Simulated model output (should be replaced with actual model interaction)
def simulate_model_output(category: str) -> list[str]:
    return [
        f"[{category}] You are in control of your life and capable of overcoming challenges."
        for _ in range(BATCH_SIZE)
    ]

# Save text to PNG image
def save_to_png(text: str, path: Path):
    font = ImageFont.truetype(FONT_PATH, 20)
    lines = text.split("\n")
    width = max(font.getlength(line) for line in lines) + 40
    height = 30 + len(lines) * 30
    image = Image.new("RGB", (int(width), height), color="white")
    draw = ImageDraw.Draw(image)
    for i, line in enumerate(lines):
        draw.text((20, 30 * i), line, font=font, fill="black")
    image.save(path)

# Save all formats per affirmation
def save_affirmation(affirmation: str, index: int, category: str):
    base_filename = f"{category}_affirmation_{index}"
    # Save text
    (OUTPUT_DIR / f"{base_filename}.txt").write_text(affirmation)
    # Save JSON
    with open(OUTPUT_DIR / f"{base_filename}.json", "w") as jf:
        json.dump({"affirmation": affirmation, "category": category}, jf)
    # Save PNG
    save_to_png(affirmation, OUTPUT_DIR / f"{base_filename}.png")
    # Log it
    with open(LOG_FILE, "a") as log:
        log.write(f"{datetime.now()} - Saved formats for: {base_filename}\n")

# Main routine
def run():
    category = "productivity"
    affirmations = simulate_model_output(category)
    for i, affirmation in enumerate(affirmations):
        save_affirmation(affirmation, i, category)

if __name__ == "__main__":
    run()
