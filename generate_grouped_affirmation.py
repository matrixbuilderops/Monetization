import os
from datetime import datetime

def create_affirmation_set(content: str, label: str = "Self_Confidence") -> str:
    # Generate unique timestamped folder name
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    base_name = f"{label}_{timestamp}"
    folder_path = os.path.join("output", base_name)
    os.makedirs(folder_path, exist_ok=True)

    # Define file paths
    txt_path = os.path.join(folder_path, f"{base_name}.txt")
    pdf_path = os.path.join(folder_path, f"{base_name}.pdf")
    png_path = os.path.join(folder_path, f"{base_name}.png")

    # Write .txt
    with open(txt_path, "w") as f:
        f.write(content)

    # Write .pdf (placeholder)
    with open(pdf_path, "wb") as f:
        f.write(b"%PDF-1.4\n%Generated affirmation content\n%%EOF")

    # Write .png (placeholder)
    with open(png_path, "wb") as f:
        f.write(b"\x89PNG\r\n\x1a\nGenerated affirmation content")

    print(f"✅ Generated: {base_name}")
    return folder_path

if __name__ == "__main__":
    example_text = """You are confident, capable, and strong.
Believe in your ability to succeed."""
    create_affirmation_set(example_text)

