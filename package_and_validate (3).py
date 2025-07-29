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

def process_folder(folder_path):
    local_passed, local_failed = [], []
    for fname in os.listdir(folder_path):
        fpath = os.path.join(folder_path, fname)
        ext = os.path.splitext(fname)[1].lower()
        if is_valid_file(fname):
            passed_check, reason = file_passes_checks(fpath, ext)
            if passed_check:
                local_passed.append(fpath)
            else:
                local_failed.append((fname, reason))
        else:
            local_failed.append((fname, "invalid extension"))
    return local_passed, local_failed

def main():
    total_passed, total_failed = [], []
    for folder in os.listdir(INPUT_DIR):
        folder_path = os.path.join(INPUT_DIR, folder)
        if os.path.isdir(folder_path):
            passed, failed = process_folder(folder_path)
            if passed:
                dest_folder = os.path.join(OUTPUT_DIR, folder)
                os.makedirs(dest_folder, exist_ok=True)
                for f in passed:
                    shutil.copy2(f, dest_folder)
            total_passed.extend(passed)
            total_failed.extend([(folder + "/" + f, r) for f, r in failed])

    print(f"✅ {len(total_passed)} files passed and grouped into '{OUTPUT_DIR}'")
    if total_failed:
        print(f"❌ {len(total_failed)} files failed validation:")
        for f, reason in total_failed:
            print(f"   - {f}: {reason}")

if __name__ == "__main__":
    main()
