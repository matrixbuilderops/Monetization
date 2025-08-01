import json
import datetime
import os
import re
import traceback

ORCHESTRATOR_VERSION = "3.0.0"

def log_action(msg):
    with open("diagnostic_action_log.log", "a", encoding="utf-8") as f:
        f.write(json.dumps({
            "timestamp": str(datetime.datetime.now()),
            "version": ORCHESTRATOR_VERSION,
            "action": msg
        }) + "\n")

def log_error(msg, exc=None, severity="ERROR"):
    with open("diagnostic_error_log.log", "a", encoding="utf-8") as f:
        entry = {
            "timestamp": str(datetime.datetime.now()),
            "version": ORCHESTRATOR_VERSION,
            "severity": severity,
            "message": msg
        }
        if exc:
            entry["exception"] = str(exc)
            entry["traceback"] = traceback.format_exc()
        f.write(json.dumps(entry, indent=2) + "\n")

def sanitize_path(filename):
    # Prevent directory traversal and invalid characters
    filename = filename.replace("..", "")
    filename = re.sub(r"[^a-zA-Z0-9_\-./]", "_", filename)
    return filename

def write_file(filename, content):
    try:
        filename = sanitize_path(filename)
        folder = os.path.dirname(filename)
        if folder and folder != "" and not os.path.exists(folder):
            os.makedirs(folder, exist_ok=True)
            log_action(f"Created folder: {folder}")
        with open(filename, "w", encoding="utf-8") as f:
            f.write(content)
        log_action(f"Wrote file: {filename}")
    except Exception as e:
        log_error(f"File write error: {filename}: {e}", exc=e)

def parse_and_store_all_blocks(output):
    filename_matches = re.findall(r"FILENAME:\s*(\S+)", output)
    code_blocks = re.findall(r"```(?:\w+)?\n(.*?)```", output, re.DOTALL)
    files_created = []
    if filename_matches and len(filename_matches) == len(code_blocks):
        # 1-to-1 mapping
        for fname, code in zip(filename_matches, code_blocks):
            write_file(fname, code)
            files_created.append(fname)
    elif filename_matches and len(filename_matches) == 1:
        # One filename, multiple blocks: enumerate
        base, ext = os.path.splitext(filename_matches[0])
        for i, code in enumerate(code_blocks):
            fname = f"{base}_block{i+1}{ext}"
            write_file(fname, code)
            files_created.append(fname)
    else:
        # No filename or mismatch: log everything, use generic names
        for i, code in enumerate(code_blocks):
            fname = f"output_block{i+1}.py"
            write_file(fname, code)
            files_created.append(fname)
    log_action(f"Files created: {files_created}")
    return files_created

# Example usage (replace or remove in production)
example_output = """
FILENAME: utils.py
```python
def add(a, b):
    return a + b