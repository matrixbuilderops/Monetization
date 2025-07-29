
from pathlib import Path
import shutil
import os
import time

# Constants for directories
BASE_DIR = Path.home() / "Documents" / "Monetization"
OUTPUT_DIR = BASE_DIR / "output"
READY_DIR = BASE_DIR / "ready_for_upload"

# Valid extensions and expected base name
VALID_EXTENSIONS = {".txt", ".pdf", ".png"}
EXPECTED_BASENAME = "Affirmations_for_Self_Confidence"

def validate_files(directory: Path) -> list[Path]:
    """
    Return list of files that pass validation: name starts with expected base and has correct extension.
    """
    valid_files = []
    for ext in VALID_EXTENSIONS:
        candidate = directory / f"{EXPECTED_BASENAME}{ext}"
        if candidate.exists() and candidate.stat().st_size > 50:  # Lowered threshold
            valid_files.append(candidate)
    return valid_files if len(valid_files) == 3 else []

def group_and_move(files: list[Path], dest_dir: Path) -> Path:
    """
    Group files into a timestamped folder and move to destination directory.
    """
    timestamp = time.strftime("%Y%m%d_%H%M%S")
    group_name = f"Self_Confidence_{timestamp}"
    group_path = OUTPUT_DIR / group_name
    group_path.mkdir(parents=True, exist_ok=True)

    for file in files:
        shutil.move(str(file), group_path / file.name)

    final_path = dest_dir / group_name
    shutil.move(str(group_path), final_path)
    return final_path

def cleanup_old_files(directory: Path, valid_set: set[str]):
    """
    Remove any leftover files from OUTPUT_DIR that match expected base name and extensions.
    """
    for ext in VALID_EXTENSIONS:
        target = directory / f"{EXPECTED_BASENAME}{ext}"
        if target.exists() and target.name not in valid_set:
            target.unlink()

def main():
    valid_files = validate_files(OUTPUT_DIR)
    if not valid_files:
        print("❌ No valid group found. Ensure all three files exist and meet size requirements.")
        return

    grouped = group_and_move(valid_files, READY_DIR)
    print(f"✅ Files grouped and moved to: {grouped}")

    # Perform cleanup
    cleanup_old_files(OUTPUT_DIR, {f.name for f in valid_files})
    print("🧹 Cleanup completed. Original files removed from output.")

if __name__ == "__main__":
    main()
