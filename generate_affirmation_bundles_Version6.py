import os
import json
import uuid
import requests
from datetime import datetime
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import subprocess

# --- CONFIGURATION ---
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

BUNDLE_SIZE = 7
MODEL_OUTPUT_DIR = Path("model_output")
FONT_PATH = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
DISCLAIMER = (
    "This content was generated and formatted using custom AI workflows by SignalCore INC. "
    "For personal use only. Redistribution is prohibited. © 2025 SignalCore INC."
)
LOG_FILE = "model_inference.log"
OLLAMA_MODEL = "mixtral:8x7b-instruct-v0.1-q6_K"

# --- STABLE DIFFUSION CONFIG ---
SD_API_URL = "http://localhost:7860/sdapi/v1/txt2img"  # Change if using another endpoint or port

def log_event(message: str):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(f"[{timestamp}] {message}\n")

def call_ollama(prompt: str) -> str:
    """Calls Ollama locally via the command line and returns output string."""
    try:
        proc = subprocess.Popen(
            ["ollama", "run", OLLAMA_MODEL],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        out, err = proc.communicate(prompt)
        if err:
            log_event(f"MODEL_ERROR: {err}")
        out = out.strip() if out else ""
        if not out:
            log_event("MODEL_WARNING: Model returned no output.")
            return "[MODEL WARNING] No output from model."
        log_event(f"MODEL_PROMPT: {prompt}\nMODEL_OUTPUT: {out}")
        return out
    except Exception as ex:
        fallback = f"[MODEL EXCEPTION] {str(ex)}"
        log_event(f"MODEL_EXCEPTION: {fallback}")
        return fallback

def generate_background_sd(prompt: str, save_path: Path, width=900, height=600, steps=30, cfg_scale=7.5):
    """Calls Stable Diffusion API to generate a background image."""
    payload = {
        "prompt": prompt,
        "width": width,
        "height": height,
        "steps": steps,
        "cfg_scale": cfg_scale,
        "sampler_index": "Euler",
        "seed": -1,
    }
    try:
        response = requests.post(SD_API_URL, json=payload)
        response.raise_for_status()
        result = response.json()
        # Most SD APIs return base64-encoded images
        import base64
        if "images" in result:
            imgdata = base64.b64decode(result["images"][0])
            with open(save_path, "wb") as f:
                f.write(imgdata)
        else:
            log_event(f"SD_API_ERROR: No images in result for prompt: {prompt}")
    except Exception as e:
        log_event(f"SD_API_ERROR: {e} for prompt: {prompt}")

def ensure_dir(path: Path):
    path.mkdir(parents=True, exist_ok=True)

def save_txt(path, affirmations):
    try:
        with open(path, "w", encoding="utf-8") as f:
            for i, aff in enumerate(affirmations, 1):
                f.write(f"{i}. {aff}\n\n")
            f.write("\n" + DISCLAIMER)
    except Exception as e:
        log_event(f"TXT_WRITE_ERROR: {e} for {path}")

def save_pdf(path, affirmations, background_path=None):
    try:
        c = canvas.Canvas(str(path), pagesize=letter)
        width, height = letter
        top = height - 80
        if background_path and os.path.exists(background_path):
            from reportlab.lib.utils import ImageReader
            bg = ImageReader(background_path)
            c.drawImage(bg, 0, 0, width=width, height=height, mask='auto')
        c.setFont("Helvetica-Bold", 20)
        c.setFillColorRGB(0.16, 0.36, 0.66)
        c.drawString(60, top, "Affirmations")
        c.setFont("Helvetica", 14)
        c.setFillColorRGB(0.14, 0.18, 0.25)
        y = top - 40
        for idx, aff in enumerate(affirmations, 1):
            c.drawString(80, y, f"{idx}. {aff}")
            y -= 30
            if y < 100:
                c.showPage()
                if background_path and os.path.exists(background_path):
                    c.drawImage(bg, 0, 0, width=width, height=height, mask='auto')
                c.setFont("Helvetica", 14)
                c.setFillColorRGB(0.14, 0.18, 0.25)
                y = top
        c.setFont("Helvetica", 8)
        c.setFillColorRGB(0.25, 0.25, 0.25)
        c.drawString(60, 40, DISCLAIMER)
        c.save()
    except Exception as e:
        log_event(f"PDF_WRITE_ERROR: {e} for {path}")

def save_png(path, affirmations, background_path=None):
    W, H = 900, 600
    margin = 40
    try:
        if background_path and os.path.exists(background_path):
            img = Image.open(background_path).convert("RGBA").resize((W, H))
        else:
            img = Image.new("RGBA", (W, H), (238, 245, 255, 255))
        d = ImageDraw.Draw(img)
        # Overlay a semi-transparent rectangle for legibility
        d.rounded_rectangle(
            [(margin, margin), (W - margin, H - margin)],
            radius=30,
            fill=(255, 255, 255, 210)
        )
        if os.path.exists(FONT_PATH):
            font = ImageFont.truetype(FONT_PATH, 26)
            title_font = ImageFont.truetype(FONT_PATH, 34)
        else:
            font = ImageFont.load_default()
            title_font = ImageFont.load_default()

        # Draw title at the top
        d.text((margin + 20, margin - 10), "Affirmations", font=title_font, fill=(30, 90, 170, 255))
        y = margin + 50
        for idx, aff in enumerate(affirmations, 1):
            d.text((margin + 20, y), f"{idx}. {aff}", font=font, fill=(22, 40, 70, 255))
            y += 45
        # Draw disclaimer at bottom
        d.text((margin + 10, H - margin - 30), DISCLAIMER, font=ImageFont.truetype(FONT_PATH, 12) if os.path.exists(FONT_PATH) else ImageFont.load_default(), fill=(70,70,70,255))
        img.convert("RGB").save(path)
    except Exception as e:
        log_event(f"PNG_WRITE_ERROR: {e} for {path}")

def save_metadata(path, data):
    try:
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)
    except Exception as e:
        log_event(f"METADATA_WRITE_ERROR: {e} for {path}")

def generate_affirmations(category, subcategory, n=BUNDLE_SIZE):
    prompt = (
        f"Generate {n} unique, inspiring affirmations for the '{subcategory}' subcategory of '{category}'. "
        f"Each affirmation should be one sentence. Output as a numbered list."
    )
    raw = call_ollama(prompt)
    # Parse model output to extract affirmations (assuming 1. ... 2. ... etc)
    lines = raw.splitlines()
    affirmations = []
    for line in lines:
        if line.strip() and line.strip()[0].isdigit():
            # remove "1. " prefix
            aff = line.strip().split(".", 1)[-1].strip()
            if aff:
                affirmations.append(aff)
        elif line.strip() and len(affirmations) < n:
            affirmations.append(line.strip())
    return affirmations[:n]

def main():
    # You can iterate all, or just one for testing
    for category, subcategories in CATEGORIES.items():
        for subcategory in subcategories:
            # === 1. Prepare paths and identifiers ===
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            uniqueid = uuid.uuid4().hex[:6]
            bundle_name = f"{category}_{subcategory}_{timestamp}_{uniqueid}"
            bundle_dir = MODEL_OUTPUT_DIR / bundle_name
            ensure_dir(bundle_dir)
            log_event(f"START_BUNDLE: {bundle_name}")

            # === 2. Start background generation in parallel ===
            background_prompt = (
                f"A beautiful, calming, high-quality background image for positive affirmations about '{subcategory}' in the context of '{category}'. "
                "No text. Trending on ArtStation, digital painting."
            )
            background_path = bundle_dir / "background.png"
            generate_background_sd(background_prompt, background_path)

            # === 3. Generate affirmations ===
            affirmations = generate_affirmations(category, subcategory, n=BUNDLE_SIZE)
            log_event(f"AFFIRMATIONS: {affirmations}")

            # === 4. Save outputs ===
            save_txt(bundle_dir / "affirmations.txt", affirmations)
            save_pdf(bundle_dir / "affirmations.pdf", affirmations, background_path)
            save_png(bundle_dir / "affirmations.png", affirmations, background_path)
            # Save metadata
            meta = {
                "category": category,
                "subcategory": subcategory,
                "timestamp": timestamp,
                "uniqueid": uniqueid,
                "affirmations": affirmations,
                "background_prompt": background_prompt
            }
            save_metadata(bundle_dir / "metadata.json", meta)
            log_event(f"DONE_BUNDLE: {bundle_name}")

if __name__ == "__main__":
    main()