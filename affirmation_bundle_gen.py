import os
import shutil
import random
import json
import subprocess
import time
from datetime import datetime
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter

# Main categories and subcategories
CATS = {
    "productivity": ["imposter_syndrome", "burnout", "workspace_focus"],
    "confidence": ["self_doubt", "public_speaking", "decision_making"],
    "gratitude": ["daily_practice", "gratitude_after_loss", "gratitude_for_body"],
    "healing": ["breakup", "trauma", "loss"],
    "focus": ["ADHD", "study_block", "digital_distraction"],
    "creativity": ["artist_block", "new_idea", "creative_confidence"],
    "happiness": ["moment_to_moment", "joyful_small_things", "inner_child"],
    "resilience": ["setback_recovery", "stress_response", "mental_toughness"],
    "self_love": ["body_image", "self_acceptance", "personal_growth"],
    "stress_relief": ["deep_breathing", "tension_release", "deadline_pressure"],
    "success": ["goals_alignment", "career_vision", "achievement_mindset"],
    "anxiety_relief": ["panic_attack", "social_anxiety", "future_worry"],
    "mindfulness": ["present_awareness", "grounding", "calm_presence"],
    "motivation": ["morning_boost", "daily_grind", "persistence"],
    "relationships": ["toxic_family", "romantic_conflict", "friendship_loss"]
}

FONT_PATH = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
OUT_BASE = Path("model_output")
READY_ETSY = Path("ready_for_upload/etsy")
READY_GUM = Path("ready_for_upload/gumroad")

MODEL_CMD = ["ollama", "run", "mixtral:8x7b-instruct-v0.1-q6_K", "--stdin"]

def ensure_dirs():
    OUT_BASE.mkdir(exist_ok=True, parents=True)
    READY_ETSY.mkdir(parents=True, exist_ok=True)
    READY_GUM.mkdir(parents=True, exist_ok=True)

def query_model(prompt: str) -> str:
    res = subprocess.run(MODEL_CMD, input=prompt.encode(), stdout=subprocess.PIPE)
    return res.stdout.decode("utf-8").strip()

def save_png(text: str, path: Path):
    img = Image.new("RGB", (800, 200), "white")
    d = ImageDraw.Draw(img)
    f = ImageFont.truetype(FONT_PATH, 24)
    d.text((20, 80), text, font=f, fill="black")
    img.save(path)

def save_pdf(text: str, path: Path):
    c = canvas.Canvas(str(path), pagesize=letter)
    c.setFont("Helvetica", 16)
    c.drawString(72, 700, text)
    c.save()

def save_txt(text: str, path: Path):
    path.write_text(text, encoding="utf-8")

def bundle_id(cat: str, sub: str) -> str:
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    return f"{cat}_{sub}_{ts}"

def run_generation():
    category = random.choice(list(CATS.keys()))
    sub = random.choice(CATS[category])
    bid = bundle_id(category, sub)

    base_batch = OUT_BASE / datetime.now().strftime("%Y%m%d_%H%M%S")
    bundle_dir = base_batch / category / sub / bid
    bundle_dir.mkdir(parents=True, exist_ok=True)

    count = random.randint(3, 7)
    metadata = {"category": category, "subcategory": sub, "bundle_id": bid, "items": []}

    for i in range(1, count+1):
        prompt = f"Write one affirmation for {category}, subcategory: {sub}."
        txt = query_model(prompt)
        fid = f"{i:03d}_{bid}"
        save_txt(txt, bundle_dir / f"{fid}.txt")
        save_pdf(txt, bundle_dir / f"{fid}.pdf")
        save_png(txt, bundle_dir / f"{fid}.png")

        metadata["items"].append({"id": i, "text": txt})
        time.sleep(0.3)

    (bundle_dir / "metadata.json").write_text(json.dumps(metadata, indent=2), encoding="utf-8")

    # Sync to upload
    dest_name = f"{category}_{sub}_{bid}"
    shutil.copytree(bundle_dir, READY_ETSY / dest_name)
    shutil.copytree(bundle_dir, READY_GUM / dest_name)
    shutil.rmtree(base_batch)

if __name__ == "__main__":
    ensure_dirs()
    run_generation()
