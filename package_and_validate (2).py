import os
import shutil

# Thresholds based on file type
MIN_SIZE = {
    ".txt": 200,
    ".pdf": 1024,
    ".png": 1024,
}

VALID_EXTENSIONS = set(MIN_SIZE.keys())
INPUT_DIR = "output"
OUTPUT_DIR = "ready_for_upload"
os.makedirs(OUTPUT_DIR, exist_ok=True)

def is_valid_file(filename):
    ext = os.path.splitext(filename)[1].lower()
    return ext in VALID_EXTENSIONS

def file_passes_checks(filepath, ext):
    try:
        size = os.path.getsize(filepath)
        return size >= MIN_SIZE[ext], f"size {size}B (min {MIN_SIZE[ext]}B)"
    except Exception as e:
        return False, f"error: {e}"

def main():
    passed, failed = [], []
    for fname in os.listdir(INPUT_DIR):
        fpath = os.path.join(INPUT_DIR, fname)
        ext = os.path.splitext(fname)[1].lower()
        if is_valid_file(fname):
            passed_check, reason = file_passes_checks(fpath, ext)
            if passed_check:
                shutil.copy2(fpath, os.path.join(OUTPUT_DIR, fname))
                passed.append(fname)
            else:
                failed.append((fname, reason))
        else:
            failed.append((fname, "invalid extension"))

    print(f"✅ {len(passed)} files passed and moved to '{OUTPUT_DIR}'")
    if failed:
        print(f"❌ {len(failed)} files failed validation:")
        for f, reason in failed:
            print(f"   - {f}: {reason}")

if __name__ == "__main__":
    main()
