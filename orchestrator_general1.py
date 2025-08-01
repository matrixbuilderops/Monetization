import subprocess
import os
import threading
import time
import sys

project_context = """
PROJECT GOAL: Build a Python CLI tool that generates Python scripts based on user commands.
CONSTRAINTS: Output valid Python code. Modular code. User-friendly CLI interface. All code must be valid Python.
NOTES: User wants minimum explanations, always output code directly.
"""

script_counter = 1

def run_mixtral(user_command):
    full_prompt = (
        f"{project_context}\n"
        f"USER COMMAND: {user_command}\n"
        "IMPORTANT: Output ONLY the complete Python code for this request. No explanations, no instructions, no comments."
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
            print(f"[!] Model error: {err_str.strip()}")
            return ""
        return out_str.strip()

    except Exception as e:
        print(f"[!] Unexpected model error: {e}")
        return ""

def write_file(filename, content):
    folder = os.path.dirname(filename)
    if folder and not os.path.exists(folder):
        os.makedirs(folder, exist_ok=True)
        print(f"[+] Created folder: {folder}")
    with open(filename, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"[+] Wrote file: {filename}")

def get_next_script_name():
    global script_counter
    while True:
        fname = f"script_{script_counter}.py"
        if not os.path.exists(fname):
            script_counter += 1
            return fname
        script_counter += 1

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

def fix_file(filename, error_message):
    prompt = (
        f"The file {filename} produced the following error when run:\n"
        f"{error_message}\n"
        f"Output ONLY the corrected code for {filename}. No explanations."
    )
    fixed_code = run_mixtral(prompt)
    if fixed_code:
        write_file(filename, fixed_code)
    else:
        print("[!] Model did not return any code.")

def main():
    global project_context
    print("== Unbreakable Project Orchestrator (General Purpose) ==")
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

        if user.startswith("write "):
            try:
                if ':' not in user:
                    print("[!] Usage: write path/to/filename.py: code prompt")
                    continue
                fname, rest = user[6:].split(":", 1)
                fname = fname.strip()
                prompt = rest.strip()
                code = run_mixtral(f"Output ONLY the complete Python code for this request, no explanations, no instructions, no comments: {prompt}")
                if code:
                    write_file(fname, code)
            except Exception as e:
                print(f"[!] Write error: {e}")
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
            files = []
            for root, dirs, filenames in os.walk(cwd):
                for fname in filenames:
                    relpath = os.path.relpath(os.path.join(root, fname), cwd)
                    files.append(relpath)
            for f in files:
                print(f)
        else:
            # All other commands are interpreted as a natural script generation prompt
            prompt = user
            code = run_mixtral(f"Output ONLY the complete Python code for this request, no explanations, no instructions, no comments: {prompt}")
            if code:
                fname = get_next_script_name()
                write_file(fname, code)
                print(f"[+] Model output saved to {fname}")
            else:
                print("[!] Model did not return any code.")

if __name__ == "__main__":
    main()