import subprocess
import os
import threading
import time
import sys
import shutil
import json
import platform

# == Configurable parameters ==
MAX_RETRIES = 3
STRICT_CODE_ONLY = True
LOG_FILE = "orchestrator.log"
CONTEXT_FILE = "project_context.json"
HISTORY_FILE = "command_history.json"
PROJECT_ROOT = os.getcwd()
SAFE_RUN = True # If True, only runs files inside PROJECT_ROOT

project_context = """
PROJECT GOAL: Build a Python CLI tool for generating images using Stable Diffusion.
CONSTRAINTS: Use only diffusers+torch. Modular code. User-friendly CLI interface. All code must be valid Python.
NOTES: User wants minimum explanations, always output code directly.
"""

command_history = []

def log(msg):
    timestamp = time.strftime("[%Y-%m-%d %H:%M:%S]")
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(f"{timestamp} {msg}\n")
    print(f"{timestamp} {msg}")

def save_context():
    data = {
        "project_context": project_context,
        "command_history": command_history
    }
    with open(CONTEXT_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)
    log("Project context and history saved.")

def load_context():
    global project_context, command_history
    if os.path.exists(CONTEXT_FILE):
        with open(CONTEXT_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
            project_context = data.get("project_context", project_context)
            command_history = data.get("command_history", [])
        log("Project context and history loaded.")
    else:
        log("No saved context found.")

def pretty_list_files(root=PROJECT_ROOT):
    print(f"Files and folders in: {root}")
    for folder, subfolders, files in os.walk(root):
        level = folder.replace(root, '').count(os.sep)
        indent = ' ' * 2 * level
        print(f"{indent}{os.path.basename(folder)}/")
        for f in files:
            path = os.path.join(folder, f)
            size = os.path.getsize(path)
            mtime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(os.path.getmtime(path)))
            print(f"{indent}  {f}  [{size} bytes, modified {mtime}]")

def tree(root=PROJECT_ROOT, prefix=""):
    """Show folder tree"""
    files = sorted(os.listdir(root))
    for idx, f in enumerate(files):
        full_path = os.path.join(root, f)
        connector = "└── " if idx == len(files)-1 else "├── "
        print(prefix + connector + f)
        if os.path.isdir(full_path):
            extension = "    " if idx == len(files)-1 else "│   "
            tree(full_path, prefix + extension)

def list_tests(root=PROJECT_ROOT):
    """List test files and summarize coverage"""
    print("Test files found:")
    for folder, _, files in os.walk(root):
        for f in files:
            if f.startswith("test_") and f.endswith(".py"):
                print(f"- {os.path.join(folder, f)}")

def check_env():
    # Python version
    print(f"Python version: {platform.python_version()}")
    # Virtualenv
    if hasattr(sys, 'real_prefix') or (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix):
        print("You are in a virtual environment.")
    else:
        print("WARNING: Not running in a virtualenv!")
    # Required packages
    for pkg in ["diffusers", "torch"]:
        try:
            __import__(pkg)
            print(f"Package '{pkg}' is installed.")
        except ImportError:
            print(f"WARNING: Required package '{pkg}' is NOT installed.")

def backup_file(filename):
    if os.path.exists(filename):
        backup_name = filename + ".bak"
        shutil.copy2(filename, backup_name)
        log(f"Backed up {filename} to {backup_name}")

def validate_code(code, required_terms=None):
    if not code:
        return False
    # Basic: must look like Python and have key imports
    if STRICT_CODE_ONLY:
        if not code.strip().startswith("import") and "def " not in code:
            return False
        if required_terms:
            for term in required_terms:
                if term not in code:
                    return False
    return True

def run_mixtral(user_command):
    full_prompt = (
        f"{project_context}\n"
        f"USER COMMAND: {user_command}\n"
        "REMINDER: Do not deviate from the project goal and constraints. Output ONLY code unless specifically asked otherwise."
    )
    cmd = ["ollama", "run", "mixtral:8x7b-instruct-v0.1-q6_K"]
    try:
        process = subprocess.Popen(
            cmd,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            bufsize=1,
        )
        process.stdin.write(full_prompt + "\n")
        process.stdin.close()

        output_lines = []
        error_lines = []
        last_output_time = time.time()
        thinking_notified = False

        def read_stream(stream, lines, name):
            for line in stream:
                lines.append(line)
                if name == "stdout":
                    sys.stdout.write(line)
                    sys.stdout.flush()
            stream.close()

        t_out = threading.Thread(target=read_stream, args=(process.stdout, output_lines, "stdout"))
        t_err = threading.Thread(target=read_stream, args=(process.stderr, error_lines, "stderr"))
        t_out.start()
        t_err.start()

        while process.poll() is None:
            if not output_lines and not thinking_notified and (time.time() - last_output_time) > 3:
                print("[.] Model is thinking…")
                thinking_notified = True
            time.sleep(0.2)

        t_out.join()
        t_err.join()

        out_str = "".join(output_lines)
        err_str = "".join(error_lines)
        if process.returncode != 0 or err_str:
            log(f"Model error: {err_str.strip()}")
            return ""
        return out_str.strip()

    except Exception as e:
        log(f"Unexpected model error: {e}")
        return ""

def write_file(filename, content):
    folder = os.path.dirname(filename)
    if folder and not os.path.exists(folder):
        os.makedirs(folder, exist_ok=True)
        log(f"Created folder: {folder}")
    if os.path.exists(filename):
        print(f"[!] File '{filename}' exists.")
        backup = input("Backup before overwrite? (y/n): ").strip().lower()
        if backup == "y":
            backup_file(filename)
    with open(filename, "w", encoding="utf-8") as f:
        f.write(content)
    log(f"Wrote file: {filename}")

def fix_file(filename, error_message):
    prompt = (
        f"The file {filename} produced the following error when run:\n"
        f"{error_message}\n"
        f"Please fix the code in {filename} to resolve this error. Output only the corrected code."
    )
    fixed_code = run_mixtral(prompt)
    if validate_code(fixed_code, ["import", "def "]):
        write_file(filename, fixed_code)
    else:
        log(f"Model did not return valid code for fix of {filename}.")

def run_file(filename, max_retries=MAX_RETRIES):
    if SAFE_RUN and not os.path.abspath(filename).startswith(PROJECT_ROOT):
        print("[!] Refusing to run scripts outside project root for safety.")
        log(f"Safe run refused for {filename}")
        return
    attempt = 0
    while attempt <= max_retries:
        try:
            result = subprocess.run(
                ["python", filename],
                capture_output=True,
                text=True
            )
            print("[stdout]")
            print(result.stdout)
            if result.stderr:
                print("[stderr]")
                print(result.stderr)
                log(f"Error running {filename}: {result.stderr}")
                attempt += 1
                if attempt > max_retries:
                    print(f"[!] Max retries reached for {filename}.")
                    log(f"Max retries reached for {filename}")
                    edit = input("Manual fix? Open file for editing? (y/n): ").strip().lower()
                    if edit == "y":
                        os.system(f"${{EDITOR:-nano}} {filename}")
                        continue
                    else:
                        break
                else:
                    print(f"[!] Attempting to auto-fix {filename} (attempt {attempt} of {max_retries})...")
                    fix_file(filename, result.stderr)
            else:
                # If tests present, run them
                test_file = f"test_{os.path.basename(filename)}"
                if os.path.exists(test_file):
                    print(f"Running tests in {test_file}...")
                    subprocess.run(["python", test_file])
                break  # Success
        except Exception as e:
            log(f"Error running file: {e}")
            break

def main():
    global project_context, command_history
    print("== Unbreakable Project Orchestrator (Perfect Edition) ==")
    print("Type 'exit' to quit. Type 'context' to view/edit/save/load project context.")
    print("Type 'list' for pretty file list, 'tree' for folder tree, 'env' for environment checks, 'tests' for test summary.")
    print("Type 'log' to show recent log entries.")
    cwd = PROJECT_ROOT
    load_context()
    while True:
        user = input(f"{cwd}> ").strip()
        command_history.append({"timestamp": time.time(), "cmd": user})
        if user.lower() in ("exit", "quit"):
            save_context()
            break
        if user.startswith("context"):
            print("Current project context:\n")
            print(project_context)
            action = input("Edit, save, or load context? (edit/save/load/none): ").strip().lower()
            if action == "edit":
                print("Paste new context (end with an empty line):")
                lines = []
                while True:
                    line = input()
                    if not line:
                        break
                    lines.append(line)
                project_context = "\n".join(lines)
                print("Context updated.")
            elif action == "save":
                save_context()
            elif action == "load":
                load_context()
            continue
        if user.startswith("write "):
            try:
                if ':' not in user:
                    print("[!] Usage: write path/to/filename.py: code prompt")
                    continue
                fname, rest = user[6:].split(":", 1)
                fname = fname.strip()
                prompt = rest.strip()
                # Strict prompt for code-only mode
                strict_prompt = (
                    f"Write a complete Python script called {fname} that does the following: {prompt}\n"
                    f"Requirements: Output only valid Python code. No explanations, markdown, or comments outside code. Use diffusers and torch. Save images as specified."
                )
                code = run_mixtral(strict_prompt)
                if validate_code(code, ["import", "def "]):
                    write_file(fname, code)
                else:
                    print("[!] Model output did not meet requirements, retrying...")
                    log("Model output did not meet requirements, retrying...")
                    # Retry 2 more times
                    for attempt in range(2):
                        code = run_mixtral("You did not follow requirements. " + strict_prompt)
                        if validate_code(code, ["import", "def "]):
                            write_file(fname, code)
                            break
            except Exception as e:
                log(f"Write error: {e}")
        elif user.startswith("show "):
            fname = user[5:].strip()
            if os.path.exists(fname):
                with open(fname, 'r', encoding='utf-8') as f:
                    print(f.read())
            else:
                print("[!] File not found.")
        elif user.startswith("run "):
            fname = user[4:].strip()
            if not os.path.exists(fname):
                print("[!] File not found.")
                continue
            run_file(fname)
        elif user.startswith("list"):
            pretty_list_files()
        elif user.startswith("tree"):
            tree()
        elif user.startswith("env"):
            check_env()
        elif user.startswith("tests"):
            list_tests()
        elif user.startswith("log"):
            if os.path.exists(LOG_FILE):
                with open(LOG_FILE, "r", encoding="utf-8") as f:
                    lines = f.readlines()[-20:]
                    print("".join(lines))
            else:
                print("No log file found.")
        else:
            response = run_mixtral(user)
            print(response)

if __name__ == "__main__":
    main()