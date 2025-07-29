import os
import json
import random
import subprocess
from datetime import datetime
from PIL import Image, ImageDraw, ImageFont
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

# === CONFIG ===
BASE_OUTPUT = "model_output"
READY_OUTPUT = "ready_for_upload"
CATEGORIES = {
    "productivity": ["burnout", "focus", "time_management", "imposter_syndrome"],
    "relationships": ["toxic_family", "breakups", "healing", "self-worth"],
    "stress_relief": ["anxiety", "relaxation", "overwhelm", "coping"],
    "confidence": ["public_speaking", "body_image", "self_doubt"],
    "gratitude": ["daily_gratitude", "gratitude_for_others"],
    "healing": ["emotional_healing", "trauma_recovery"],
    "creativity": ["creative_block", "artistic_expression"],
    "happiness": ["joy_cultivation", "daily_happiness"],
    "resilience": ["bouncing_back", "inner_strength"],
    "self_focus": ["personal_growth", "self_reflection"],
    "self_love": ["acceptance", "self_worth"],
    "success": ["goal_setting", "achievement_mindset"],
    "anxiety_relief": ["calm_thoughts", "peaceful_mind"],
    "mindfulness": ["present_moment", "awareness"],
    "motivation": ["get_started", "keep_going"]
}
FONTPATH = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
MODEL_CMD = ["ollama", "run", "mistral:8x7b-instruct-v0.1-q6_K", "--stdin"]

# === UTILITIES ===
def ensure_dir(path: str):
    os.makedirs(path, exist_ok=True)

def call_model(prompt: str) -> str:
    result = subprocess.run(MODEL_CMD, input=prompt.encode(), stdout=subprocess.PIPE)
    return result.stdout.decode().strip()

def generate_affirmation(category: str, subcategory: str) -> str:
    prompt = f"Write a positive affirmation for someone struggling with {subcategory.replace('_', ' ')}."
    return call_model(prompt)

def save_text_file(path: str, text: str):
    with open(path, 'w') as f:
        f.write(text + "\n\n" + FOOTER)

def save_json_file(path: str, data: dict):
    with open(path, 'w') as f:
        json.dump(data, f, indent=2)

def save_image(path: str, text: str):
    img = Image.new('RGB', (800, 400), color=(255, 255, 255))
    draw = ImageDraw.Draw(img)
    try:
        font = ImageFont.truetype(FONTPATH, 24)
    except:
        font = ImageFont.load_default()
    draw.text((50, 180), text, fill=(0, 0, 0), font=font)
    draw.text((10, 370), FOOTER, fill=(120, 120, 120), font=font)
    img.save(path)

def save_pdf(path: str, text: str):
    c = canvas.Canvas(path, pagesize=letter)
    width, height = letter
    c.setFont("Helvetica", 14)
    c.drawString(100, height / 2, text)
    c.setFont("Helvetica", 8)
    c.drawString(50, 30, FOOTER)
    c.save()

FOOTER = (
    "This content was generated and formatted using custom AI workflows by SignalCore LLC. "
    "For personal use only. Redistribution is prohibited. \u00a9 2025 SignalCore LLC."
)

# === MAIN ===
def run_bundle_generation(num_per_bundle=7):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    for category, subcats in CATEGORIES.items():
        for sub in subcats:
            bundle_dir = os.path.join(BASE_OUTPUT, f"{timestamp}_{category}_{sub}")
            ensure_dir(bundle_dir)
            for i in range(num_per_bundle):
                affirmation = generate_affirmation(category, sub)
                id_tag = f"{category}_{sub}_{i+1}"

                # Save all formats
                txt_path = os.path.join(bundle_dir, f"{id_tag}.txt")
                png_path = os.path.join(bundle_dir, f"{id_tag}.png")
                pdf_path = os.path.join(bundle_dir, f"{id_tag}.pdf")
                json_path = os.path.join(bundle_dir, f"{id_tag}.json")

                save_text_file(txt_path, affirmation)
                save_image(png_path, affirmation)
                save_pdf(pdf_path, affirmation)
                save_json_file(json_path, {
                    "id": id_tag,
                    "category": category,
                    "subcategory": sub,
                    "affirmation": affirmation
                })

            # Move entire bundle to ready folder
            dest_ready = os.path.join(READY_OUTPUT, os.path.basename(bundle_dir))
            ensure_dir(READY_OUTPUT)
            os.rename(bundle_dir, dest_ready)

if __name__ == "__main__":
    run_bundle_generation()
