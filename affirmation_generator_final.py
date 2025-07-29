import os
import subprocess
import json
from datetime import datetime
from PIL import Image, ImageDraw, ImageFont
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

# === CONFIG ===
BASE_OUTPUT = "model_output"
READY_UPLOAD = "ready_for_upload"
FONTPATH = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
LEGAL_FOOTER = ("This content was generated and formatted using custom AI workflows by SignalCore LLC\n"
                "For personal use only. Redistribution is prohibited.\n"
                "© 2025 SignalCore LLC. All rights reserved.")
OLLAMA_MODEL = "mixtral:8x7b-instruct-v0.1-q6_K"
NUM_AFFIRMATIONS = 7

# === FULL CATEGORY MAP ===
CATEGORIES = {
    "productivity": ["burnout", "focus", "time management", "imposter syndrome"],
    "confidence": ["self-esteem", "public speaking", "courage"],
    "gratitude": ["daily gratitude", "thankfulness"],
    "healing": ["emotional", "physical", "spiritual"],
    "focus": ["attention", "clarity", "goals"],
    "creativity": ["artistic", "innovation", "expression"],
    "happiness": ["joy", "contentment", "lightness"],
    "resilience": ["hard times", "adversity", "bounce back"],
    "self_focus": ["reflection", "grounding"],
    "self_love": ["worth", "kindness"],
    "stress_relief": ["anxiety", "overwhelm", "coping"],
    "success": ["achievement", "ambition"],
    "anxiety_relief": ["nervousness", "peace of mind"],
    "mindfulness": ["present moment", "stillness"],
    "motivation": ["daily push", "energy", "momentum"],
    "relationships": ["toxic family", "breakups", "healing", "self-worth"]
}

# === UTILITIES ===
def ensure_dir(path: str):
    os.makedirs(path, exist_ok=True)

def call_model(prompt: str) -> str:
    result = subprocess.run(
        ["ollama", "run", OLLAMA_MODEL],
        input=prompt.encode(),
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    output = result.stdout.decode().strip()
    return output.split("\n")[0]  # use only first line

def save_text(path: str, content: str):
    with open(path, 'w') as f:
        f.write(content + "\n" + LEGAL_FOOTER)

def save_image(path: str, content: str):
    img = Image.new('RGB', (800, 400), color=(255, 255, 255))
    draw = ImageDraw.Draw(img)
    try:
        font = ImageFont.truetype(FONTPATH, 22)
    except:
        font = ImageFont.load_default()
    draw.text((50, 150), content, fill=(0, 0, 0), font=font)
    draw.text((20, 360), LEGAL_FOOTER, fill=(100, 100, 100), font=font)
    img.save(path)

def save_pdf(path: str, content: str):
    c = canvas.Canvas(path, pagesize=letter)
    width, height = letter
    c.setFont("Helvetica", 14)
    c.drawString(100, height / 2, content)
    c.setFont("Helvetica", 8)
    c.drawString(50, 30, LEGAL_FOOTER)
    c.save()

def generate_affirmations():
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    for cat, subcats in CATEGORIES.items():
        for sub in subcats:
            bundle_dir = os.path.join(BASE_OUTPUT, f"{timestamp}_{cat}_{sub.replace(' ', '_')}")
            ensure_dir(bundle_dir)
            for i in range(NUM_AFFIRMATIONS):
                prompt = f"Give me one positive affirmation about {sub} in the context of {cat}."
                affirm = call_model(prompt)
                affirm_id = f"{cat}_{sub}_{i+1}"
                
                txt_path = os.path.join(bundle_dir, f"{affirm_id}.txt")
                png_path = os.path.join(bundle_dir, f"{affirm_id}.png")
                pdf_path = os.path.join(bundle_dir, f"{affirm_id}.pdf")
                json_path = os.path.join(bundle_dir, f"{affirm_id}.json")

                save_text(txt_path, affirm)
                save_image(png_path, affirm)
                save_pdf(pdf_path, affirm)
                with open(json_path, 'w') as jf:
                    json.dump({
                        "id": affirm_id,
                        "category": cat,
                        "subcategory": sub,
                        "affirmation": affirm
                    }, jf, indent=2)

            for platform in ["etsy", "gumroad"]:
                platform_dir = os.path.join(READY_UPLOAD, platform, os.path.basename(bundle_dir))
                ensure_dir(os.path.dirname(platform_dir))
                os.rename(bundle_dir, platform_dir)

if __name__ == "__main__":
    generate_affirmations()
