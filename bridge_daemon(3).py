import os
import random
import subprocess
import time
from datetime import datetime
from typing import List
from PIL import Image, ImageDraw, ImageFont
from reportlab.pdfgen import canvas

OUTPUT_DIR = "./model_output"
READY_DIR = "./ready_for_upload"
LOG_FILE = "./bridge_log.txt"
MODEL_NAME = "mixtral:8x7b-instruct-v0.1-q6_K"

CATEGORIES = [
    "career affirmations",
    "self-love affirmations",
    "confidence affirmations",
    "financial abundance affirmations",
    "relationship affirmations",
    "mental health affirmations",
    "overcoming anxiety affirmations",
    "daily motivation affirmations",
    "gratitude affirmations",
    "productivity affirmations",
    "social confidence affirmations",
    "healing from trauma affirmations",
    "motivation to exercise affirmations",
    "letting go of the past affirmations",
    "spiritual growth affirmations",
]

def log_event(message: str):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(LOG_FILE, "a") as f:
        f.write(f"[{timestamp}] {message}\n")

def generate_from_model(prompt: str) -> List[str]:
    process = subprocess.Popen(
        ["ollama", "run", MODEL_NAME],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
    stdout, stderr = process.communicate(input=prompt)
    if stderr:
        log_event(f"Model error: {stderr.strip()}")
    return [line.strip() for line in stdout.split("\n") if line.strip()]

def save_text(content: str, filepath: str):
    with open(filepath + ".txt", "w") as f:
        f.write(content)

def save_pdf(content: str, filepath: str):
    c = canvas.Canvas(filepath + ".pdf")
    c.drawString(100, 750, content)
    c.save()

def save_image(content: str, filepath: str):
    img = Image.new("RGB", (800, 200), color=(255, 255, 255))
    draw = ImageDraw.Draw(img)
    try:
        font = ImageFont.truetype("arial.ttf", 20)
    except IOError:
        font = ImageFont.load_default()
    draw.text((10, 90), content, fill=(0, 0, 0), font=font)
    img.save(filepath + ".png")

def main(prompt_type: str = None, num_outputs: int = None):
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    os.makedirs(os.path.join(READY_DIR, "etsy"), exist_ok=True)
    os.makedirs(os.path.join(READY_DIR, "gumtree"), exist_ok=True)

    if not prompt_type:
        prompt_type = random.choice(CATEGORIES)
    if not num_outputs:
        num_outputs = random.randint(3, 7)
    base_prompt = f"Generate {num_outputs} unique {prompt_type}."
    results = generate_from_model(base_prompt)

    for i, affirmation in enumerate(results[:num_outputs]):
        timestamp = int(time.time())
        file_base = f"affirmation_{prompt_type.replace(' ', '_')}_{timestamp}_{i}"
        raw_path = os.path.join(OUTPUT_DIR, file_base)
        etsy_path = os.path.join(READY_DIR, "etsy", file_base)
        gumtree_path = os.path.join(READY_DIR, "gumtree", file_base)

        save_text(affirmation, raw_path)
        save_pdf(affirmation, raw_path)
        save_image(affirmation, raw_path)

        save_text(affirmation, etsy_path)
        save_pdf(affirmation, etsy_path)
        save_image(affirmation, etsy_path)

        save_text(affirmation, gumtree_path)
        save_pdf(affirmation, gumtree_path)
        save_image(affirmation, gumtree_path)

        log_event(f"Saved all formats for: {file_base} in model_output and ready_for_upload")

if __name__ == "__main__":
    main()
