import os
import time
from datetime import datetime

OUTPUT_DIR = "output"
UPLOAD_DIR = "ready_for_upload"

def create_affirmation_set(content: str) -> str:
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    os.makedirs(UPLOAD_DIR, exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    base_name = "Self_Confidence_" + timestamp
    txt_name = base_name + ".txt"
    pdf_name = base_name + ".pdf"
    png_name = base_name + ".png"

    txt_path = os.path.join(OUTPUT_DIR, txt_name)
    pdf_path = os.path.join(OUTPUT_DIR, pdf_name)
    png_path = os.path.join(OUTPUT_DIR, png_name)

    with open(txt_path, "w") as f:
        f.write(content)

    with open(pdf_path, "wb") as f:
        f.write(b"%PDF-1.4\nGenerated affirmation content\n%%EOF")

    with open(png_path, "wb") as f:
        f.write(b"\x89PNG\r\n\x1a\nGenerated affirmation content")

    # Create grouped folder and move files there
    folder_path = os.path.join(OUTPUT_DIR, base_name)
    os.makedirs(folder_path, exist_ok=True)

    for path in [txt_path, pdf_path, png_path]:
        os.rename(path, os.path.join(folder_path, os.path.basename(path)))

    # Move the entire folder to ready_for_upload
    dest_folder = os.path.join(UPLOAD_DIR, base_name)
    if os.path.exists(dest_folder):
        for file in os.listdir(dest_folder):
            os.remove(os.path.join(dest_folder, file))
        os.rmdir(dest_folder)
    os.rename(folder_path, dest_folder)

    print("✅ Grouped and moved to ready_for_upload:", dest_folder)
    return dest_folder

if __name__ == "__main__":
    example_text = """You are confident, capable, and strong.
Believe in your ability to succeed."""
    create_affirmation_set(example_text)
