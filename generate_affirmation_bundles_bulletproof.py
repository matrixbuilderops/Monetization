import os
import json
import shutil
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

OUTPUT_ROOT = Path("ready_for_upload")
PLATFORMS = ["etsy", "gumroad"]
BUNDLE_SIZE = 7
FONT_PATH = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
DISCLAIMER = (
    "This content was generated and formatted using custom AI workflows by SignalCore INC. "
    "For personal use only. Redistribution is prohibited. © 2025 SignalCore INC."
)
LOG_FILE = "model_inference.log"
OLLAMA_MODEL = "mixtral:8x7b-instruct-v0.1-q6_K"

def log_event(message: str):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(f"[{timestamp}] {message}\n")

def call_ollama(prompt: str) -> str:
    """
    Calls Ollama locally via the command line, mimicking a real user:
    - Starts process
    - Sends prompt to stdin
    - Closes stdin (signals EOF)
    - Reads output
    """
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

def ensure_dir(path):
    os.makedirs(path, exist_ok=True)

def save_txt(path, text):
    try:
        with open(path, "w", encoding="utf-8") as f:
            f.write(text + "\n\n" + DISCLAIMER)
    except Exception as e:
        log_event(f"TXT_WRITE_ERROR: {e} for {path}")

def save_pdf(path, text):
    try:
        c = canvas.Canvas(str(path), pagesize=letter)
        width, height = letter
        c.setFont("Helvetica-Bold", 16)
        c.drawString(60, height - 120, text)
        c.setFont("Helvetica", 8)
        c.drawString(60, 40, DISCLAIMER)
        c.save()
    except Exception as e:
        log_event(f"PDF_WRITE_ERROR: {e} for {path}")

def save_png(path, text):
    W, H = 800, 400
    img = Image.new("RGB", (W, H), (255, 255, 255))
    d = ImageDraw.Draw(img)
    try:
        if os.path.exists(FONT_PATH):
            font = ImageFont.truetype(FONT_PATH, 24)
            footer_font = ImageFont.truetype(FONT_PATH, 14)
        else:
            font = ImageFont.load_default()
            footer_font = ImageFont.load_default()
            log_event(f"FONT_WARNING: {FONT_PATH} not found. Using default font.")
    except Exception as e:
        font = ImageFont.load_default()
        footer_font = ImageFont.load_default()
        log_event(f"FONT_EXCEPTION: {e}. Using default font.")
    try:
        d.text((50, 150), text, fill=(0, 0, 0), font=font)
        d.text((10, H - 35), DISCLAIMER, fill=(120, 120, 120), font=footer_font)
        img.save(path)
    except Exception as e:
        log_event(f"PNG_WRITE_ERROR: {e} for {path}")

def generate_bundle(category, subcategory, timestamp):
    base_name = f"{category}_{subcategory}_{timestamp}"
    files = []
    affirmations = []
    for i in range(BUNDLE_SIZE):
        prompt = (
            f"Write a unique positive affirmation for the following category and subcategory.\n"
            f"Category: {category}\nSubcategory: {subcategory}\n"
            f"Format as a standalone, powerful, one-sentence affirmation."
        )
        aff = call_ollama(prompt)
        txt_path = f"{base_name}_{i+1}.txt"
        pdf_path = f"{base_name}_{i+1}.pdf"
        png_path = f"{base_name}_{i+1}.png"
        # Try to create each file, only append if creation was successful
        created_files = []
        try:
            save_txt(txt_path, aff)
            if os.path.exists(txt_path):
                created_files.append(txt_path)
        except Exception as e:
            log_event(f"TXT_CREATE_ERROR: {e} for {txt_path}")
        try:
            save_pdf(pdf_path, aff)
            if os.path.exists(pdf_path):
                created_files.append(pdf_path)
        except Exception as e:
            log_event(f"PDF_CREATE_ERROR: {e} for {pdf_path}")
        try:
            save_png(png_path, aff)
            if os.path.exists(png_path):
                created_files.append(png_path)
        except Exception as e:
            log_event(f"PNG_CREATE_ERROR: {e} for {png_path}")
        files.append((txt_path, pdf_path, png_path))
        affirmations.append({"index": i+1, "text": aff})
    meta = {
        "category": category,
        "subcategory": subcategory,
        "timestamp": timestamp,
        "disclaimer": DISCLAIMER,
        "affirmations": affirmations
    }
    meta_path = f"{base_name}_metadata.json"
    try:
        with open(meta_path, "w", encoding="utf-8") as f:
            json.dump(meta, f, indent=2)
    except Exception as e:
        log_event(f"METADATA_WRITE_ERROR: {e} for {meta_path}")
    return files, meta_path

def organize_bundle(category, subcategory, timestamp, files, metadata):
    for platform in PLATFORMS:
        bundle_dir = OUTPUT_ROOT / platform / f"{category}_{subcategory}_{timestamp}"
        ensure_dir(bundle_dir)
        for txt, pdf, png in files:
            for fpath in [txt, pdf, png]:
                if os.path.exists(fpath):
                    try:
                        shutil.move(fpath, bundle_dir / os.path.basename(fpath))
                        log_event(f"FILE_MOVED: {fpath} -> {bundle_dir / os.path.basename(fpath)}")
                    except Exception as e:
                        log_event(f"FILE_MOVE_ERROR: {e} for {fpath}")
                else:
                    log_event(f"FILE_NOT_FOUND: {fpath}")
        if os.path.exists(metadata):
            try:
                shutil.move(metadata, bundle_dir / os.path.basename(metadata))
                log_event(f"METADATA_MOVED: {metadata} -> {bundle_dir / os.path.basename(metadata)}")
            except Exception as e:
                log_event(f"METADATA_MOVE_ERROR: {e} for {metadata}")
        else:
            log_event(f"METADATA_NOT_FOUND: {metadata}")

def main():
    now = datetime.now().strftime("%Y%m%d_%H%M%S")
    for category, sublist in CATEGORIES.items():
        for subcategory in sublist:
            try:
                files, meta = generate_bundle(category, subcategory, now)
                organize_bundle(category, subcategory, now, files, meta)
                print(f"Generated bundle: {category}/{subcategory} at {now}")
            except Exception as e:
                log_event(f"FATAL_ERROR: {e} for {category} / {subcategory}")
                print(f"Error in bundle {category}/{subcategory}: {e} (see log)")

if __name__ == "__main__":
    main()