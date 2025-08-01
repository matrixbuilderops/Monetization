import subprocess
import os
import threading
import time
import sys
import re

project_context = """
PROJECT GOAL: Build a Python CLI tool for generating images using Stable Diffusion.
CONSTRAINTS: Use only diffusers+torch. Modular code. User-friendly CLI interface. All code must be valid Python.
NOTES: User wants minimum explanations, always output code directly.
"""

def parse_and_store_all_blocks(output):
    filename_matches = re.findall(r"FILENAME:\s*(\S+)", output)
    code_blocks = re.findall(r"```(?:\w+)?\n(.*?)```", output, re.DOTALL)
    files_created = []
    def write_file(filename, content):
        folder = os.path.dirname(filename)
        if folder and not os.path.exists(folder):
            os.makedirs(folder, exist_ok=True)
            print(f"[+] Created folder: {folder}")
        with open(filename, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"[+] Wrote file: {filename}")
    if filename_matches and len(filename_matches) == len(code_blocks):
        for fname, code in zip(filename_matches, code_blocks):
            write_file(fname, code)
            files_created.append(fname)
    elif filename_matches and len(filename_matches) == 1:
        base, ext = os.path.splitext(filename_matches[0])
        for i, code in enumerate(code_blocks):
            fname = f"{base}_block{i+1}{ext}"
            write_file(fname, code)
            files_created.append(fname)
    else:
        for i, code in enumerate(code_blocks):
            fname = f"output_block{i+1}.py"
            write_file(fname, code)
            files_created.append(fname)
    if files_created:
        print(f"[+] Files created: {files_created}")
    return files_created

def run_mixtral(user_command):
    full_prompt = (
        f"{project_context}\n"
        f"USER COMMAND: {user_command}\n"
        "REMINDER: Do not deviate from the project goal and constraints. On pain of death, do not output anything but actionable code or direct answers that move the project forward."
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
        # Automatically parse and save code blocks as files!
        parse_and_store_all_blocks(out_str)
        if process.returncode != 0 or err_str:
            print(f"[!] Model error: {err_str.strip()}")
            return ""
        return out_str.strip()

    except Exception as e:
        print(f"[!] Unexpected model error: {e}")
        return ""

def fix_file(filename, error_message):
    prompt = (
        f"The file {filename} produced the following error when run:\n"
        f"{error_message}\n"
        f"Please fix the code in {filename} to resolve this error. Output only the corrected code."
    )
    fixed_code = run_mixtral(prompt)
    # The fixed code will be auto-saved as a file if it contains a FILENAME/code block!

def run_file(filename, max_retries=3):
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
                attempt += 1
                if attempt > max_retries:
                    print(f"[!] Max retries reached for {filename}.")
                    break
                else:
                    print(f"[!] Attempting to auto-fix {filename} (attempt {attempt} of {max_retries})...")
                    fix_file(filename, result.stderr)
            else:
                break  # Success
        except Exception as e:
            print(f"[!] Error running file: {e}")
            break

def main():
    global project_context
    print("== Unbreakable Project Orchestrator with Autosave ==")
    print("Type 'exit' to quit. Type 'context' to view/edit the current project context.")
    cwd = os.getcwd()
    while True:
        user = input(f"{cwd}> ").strip()
        if user.lower() in ("exit", "quit"):
            break

        if user.startswith("context"):
            print("Current project context:\n")
            print(project_context)
            edit = input("Edit context? (y/n): ").strip().lower()
            if edit == "y":
                print("Paste new context (end with an empty line):")
                lines = []
                while True:
                    line = input()
                    if not line:
                        break
                    lines.append(line)
                project_context = "\n".join(lines)
                print("Context updated.")
            continue

        elif user.startswith("run "):
            fname = user[4:].strip()
            if not os.path.exists(fname):
                print("[!] File not found.")
                continue
            run_file(fname)
        elif user.startswith("show "):
            fname = user[5:].strip()
            if os.path.exists(fname):
                with open(fname, 'r', encoding='utf-8') as f:
                    print(f.read())
            else:
                print("[!] File not found.")
        elif user.startswith("list"):
            files = []
            for root, dirs, filenames in os.walk(cwd):
                for fname in filenames:
                    relpath = os.path.relpath(os.path.join(root, fname), cwd)
                    files.append(relpath)
            for f in files:
                print(f)
        else:
            # All prompts go to model, and outputs (code) are auto-saved!
            response = run_mixtral(user)
            print(response)

if __name__ == "__main__":
    main()