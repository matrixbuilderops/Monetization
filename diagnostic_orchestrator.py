import subprocess
import os
import threading
import time
import sys
import re
import traceback
import datetime

# Configurable verbosity
VERBOSE = True
RAW_OUTPUT_LOG = "diagnostic_raw_output.log"
PARSE_LOG = "diagnostic_parse_log.log"
ERROR_LOG = "diagnostic_error_log.log"
ACTION_LOG = "diagnostic_action_log.log"

project_context = """
PROJECT GOAL: General-purpose Python CLI assistant to generate, view, run, and fix Python scripts/files via local AI model.
CONSTRAINTS: Always start output with 'FILENAME: <filename>' on a separate line. Then code in triple backticks (```python ... ```). Logs in <LOG>...</LOG>. Errors in <ERROR>...</ERROR>. Never explain unless asked.
NOTES: User may request anything. Always follow protocol and autosave outputs.
"""

def log_to_file(logname, content):
    with open(logname, "a", encoding="utf-8") as f:
        f.write(f"[{datetime.datetime.now()}]\n{content}\n---\n")

def run_mixtral(user_command):
    full_prompt = (
        f"{project_context}\n"
        f"USER COMMAND: {user_command}\n"
        "REMINDER: Do not deviate from the project goal and constraints. Output only actionable code or direct answers."
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
                if VERBOSE and name == "stdout":
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
        # Log raw output
        log_to_file(RAW_OUTPUT_LOG, out_str)
        if process.returncode != 0 or err_str:
            log_to_file(ERROR_LOG, f"Model error: {err_str.strip()}")
            print(f"[!] Model error: {err_str.strip()}")
            return ""
        return out_str.strip()

    except Exception as e:
        log_to_file(ERROR_LOG, f"Unexpected model error: {e}\n{traceback.format_exc()}")
        print(f"[!] Unexpected model error: {e}")
        return ""

def parse_model_output(output):
    # Diagnostics: show what we're parsing
    if VERBOSE:
        print("\n[Diagnostics] Parsing model output:")
        print(output)
    try:
        match = re.search(r"FILENAME:\s*(\S+)", output)
        filename = match.group(1) if match else None
        code_blocks = re.findall(r"```(?:python)?\n(.*?)```", output, re.DOTALL)
        logs = re.findall(r"<LOG>(.*?)</LOG>", output, re.DOTALL)
        errors = re.findall(r"<ERROR>(.*?)</ERROR>", output, re.DOTALL)
        parse_result = {
            'filename': filename,
            'code': code_blocks,
            'logs': logs,
            'errors': errors
        }
        log_to_file(PARSE_LOG, f"Parse Input:\n{output}\nParse Output:\n{parse_result}")
        return parse_result
    except Exception as e:
        log_to_file(ERROR_LOG, f"Parse error: {e}\n{traceback.format_exc()}")
        print(f"[!] Parse error: {e}")
        return {'filename': None, 'code': [], 'logs': [], 'errors': []}

def clarify_output(output):
    clarification_prompt = (
        f"Clarify and reformat the following output per protocol (start with FILENAME, then code in triple backticks, logs in <LOG>, errors in <ERROR>):\n{output}\n"
        "Only output using the correct protocol tags."
    )
    clarified = run_mixtral(clarification_prompt)
    return clarified

def write_file(filename, content):
    try:
        folder = os.path.dirname(filename)
        if folder and not os.path.exists(folder):
            os.makedirs(folder, exist_ok=True)
            print(f"[+] Created folder: {folder}")
            log_to_file(ACTION_LOG, f"Created folder: {folder}")
        with open(filename, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"[+] Wrote file: {filename}")
        log_to_file(ACTION_LOG, f"Wrote file: {filename}\nContent:\n{content}")
    except Exception as e:
        log_to_file(ERROR_LOG, f"File write error: {filename}: {e}\n{traceback.format_exc()}")
        print(f"[!] File write error: {filename}: {e}")

def fix_file(filename, error_message):
    prompt = (
        f"The file {filename} produced the following error when run:\n"
        f"{error_message}\n"
        f"Please fix the code in {filename} to resolve this error. Output only the corrected code in triple backticks and always start with FILENAME marker."
    )
    fixed_code = run_mixtral(prompt)
    parsed = parse_model_output(fixed_code)
    if parsed['filename'] and parsed['code']:
        write_file(parsed['filename'], parsed['code'][0])
    else:
        print("[!] Model did not return filename or code block when fixing.")
        log_to_file(ERROR_LOG, f"Missing filename/code when fixing: {fixed_code}")

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
            log_to_file(ACTION_LOG, f"Run file: {filename}\nstdout:\n{result.stdout}")
            if result.stderr:
                print("[stderr]")
                print(result.stderr)
                log_to_file(ACTION_LOG, f"Run file: {filename}\nstderr:\n{result.stderr}")
                attempt += 1
                if attempt > max_retries:
                    print(f"[!] Max retries reached for {filename}.")
                    log_to_file(ERROR_LOG, f"Max retries reached for {filename} on error:\n{result.stderr}")
                    break
                else:
                    print(f"[!] Attempting to auto-fix {filename} (attempt {attempt} of {max_retries})...")
                    fix_file(filename, result.stderr)
            else:
                break  # Success
        except Exception as e:
            log_to_file(ERROR_LOG, f"Error running file: {filename}: {e}\n{traceback.format_exc()}")
            print(f"[!] Error running file: {e}")
            break

def main():
    global project_context
    print("== Diagnostic Python CLI Orchestrator ==")
    print("Type 'exit' to quit. Type 'context' to view/edit the current project context.")
    print("Type 'verbose on' or 'verbose off' to adjust diagnostics output.")
    cwd = os.getcwd()
    while True:
        try:
            user = input(f"{cwd}> ").strip()
        except EOFError:
            print("\n[!] EOF received, exiting.")
            break
        if user.lower() in ("exit", "quit"):
            break

        if user.lower() == "verbose on":
            global VERBOSE
            VERBOSE = True
            print("[*] Verbose mode ON.")
            continue
        if user.lower() == "verbose off":
            VERBOSE = False
            print("[*] Verbose mode OFF.")
            continue

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
                code_output = run_mixtral(f"Write a complete Python script called {fname} that does the following: {prompt} Always start with FILENAME marker and output code in triple backticks.")
                parsed = parse_model_output(code_output)
                # Diagnostics
                print("[Diagnostics] Parse result for write:")
                print(parsed)
                if not (parsed['filename'] and parsed['code']):
                    print("[!] Output missing filename or code block. Asking model to clarify...")
                    clarified = clarify_output(code_output)
                    parsed = parse_model_output(clarified)
                    print("[Diagnostics] Parse result after clarification:")
                    print(parsed)
                if parsed['filename'] and parsed['code']:
                    write_file(parsed['filename'], parsed['code'][0])
                else:
                    print("[!] Model did not return filename or code block after clarification.")
            except Exception as e:
                log_to_file(ERROR_LOG, f"Write error: {e}\n{traceback.format_exc()}")
                print(f"[!] Write error: {e}")
        elif user.startswith("show "):
            fname = user[5:].strip()
            if os.path.exists(fname):
                try:
                    with open(fname, 'r', encoding='utf-8') as f:
                        content = f.read()
                        print(content)
                        log_to_file(ACTION_LOG, f"Show file: {fname}\nContent:\n{content}")
                except Exception as e:
                    log_to_file(ERROR_LOG, f"Show file error: {fname}: {e}\n{traceback.format_exc()}")
                    print(f"[!] Show file error: {fname}: {e}")
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
            log_to_file(ACTION_LOG, f"List files:\n" + "\n".join(files))
        else:
            response = run_mixtral(user)
            parsed = parse_model_output(response)
            print("[Diagnostics] Parse result for general command:")
            print(parsed)
            # Print logs, errors, code separately
            if parsed['logs']:
                print("[LOGS]")
                for log in parsed['logs']:
                    print(log)
            if parsed['errors']:
                print("[ERRORS]")
                for err in parsed['errors']:
                    print(err)
            if parsed['code']:
                print("[CODE]")
                for code in parsed['code']:
                    print(code)
            # If nothing matched, clarify
            if not (parsed['logs'] or parsed['errors'] or parsed['code']):
                print("[!] Output was ambiguous. Asking model to clarify...")
                clarified = clarify_output(response)
                parsed = parse_model_output(clarified)
                print("[Diagnostics] Parse result after clarification:")
                print(parsed)
                # Print clarified output
                if parsed['logs']:
                    print("[LOGS]")
                    for log in parsed['logs']:
                        print(log)
                if parsed['errors']:
                    print("[ERRORS]")
                    for err in parsed['errors']:
                        print(err)
                if parsed['code']:
                    print("[CODE]")
                    for code in parsed['code']:
                        print(code)

if __name__ == "__main__":
    main()