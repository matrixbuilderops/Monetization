import os
import shutil

VALID_EXTENSIONS = {".pdf", ".txt", ".png"}
INPUT_DIR = "output"
OUTPUT_DIR = "ready_for_upload"
os.makedirs(OUTPUT_DIR, exist_ok=True)

def is_valid_file(filename):
    ext = os.path.splitext(filename)[1].lower()
    return ext in VALID_EXTENSIONS

def file_passes_basic_checks(filepath):
    return os.path.isfile(filepath) and os.path.getsize(filepath) > 500

def main():
    passed, failed = [], []
    for fname in os.listdir(INPUT_DIR):
        fpath = os.path.join(INPUT_DIR, fname)
        if is_valid_file(fname) and file_passes_basic_checks(fpath):
            shutil.copy2(fpath, os.path.join(OUTPUT_DIR, fname))
            passed.append(fname)
        else:
            failed.append(fname)

    print(f"✅ {len(passed)} files passed and moved to '{OUTPUT_DIR}'")
    if failed:
        print(f"❌ {len(failed)} files failed validation:")
        for f in failed:
            print(f"   - {f}")

if __name__ == "__main__":
    main()
