import subprocess
import os
import shlex
import ast
import threading
import queue

def run_mixtral(prompt, timeout=120):
    """Send prompt to Mixtral model via Ollama and return response with error handling."""
    cmd = "ollama run mixtral:8x7b-instruct-v0.1-q6_K"
    try:
        process = subprocess.Popen(
            shlex.split(cmd),
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        out, err = process.communicate(prompt, timeout=timeout)
        if process.returncode != 0 or err:
            print(f"[!] Model error: {err.strip()}")
            return ""
        return out.strip()
    except FileNotFoundError:
        print("[!] ollama not found. Is it installed and on your PATH?")
        return ""
    except subprocess.TimeoutExpired:
        print("[!] Model call timed out.")
        return ""
    except Exception as e:
        print(f"[!] Unexpected model error: {e}")
        return ""

def is_probably_python(code):
    """Check if code is valid Python."""
    try:
        ast.parse(code)
        return True
    except Exception:
        return False

def syntax_check(filename):
    try:
        subprocess.check_output(["python", "-m", "py_compile", filename], stderr=subprocess.STDOUT)
        return True, ""
    except subprocess.CalledProcessError as e:
        return False, e.output.decode()

def lint_check(filename):
    try:
        subprocess.check_output(["flake8", filename], stderr=subprocess.STDOUT)
        return True, ""
    except FileNotFoundError:
        return True, ""  # flake8 not installed, skip
    except subprocess.CalledProcessError as e:
        return False, e.output.decode()

def type_check(filename):
    try:
        subprocess.check_output(["mypy", filename], stderr=subprocess.STDOUT)
        return True, ""
    except FileNotFoundError:
        return True, ""  # mypy not installed, skip
    except subprocess.CalledProcessError as e:
        return False, e.output.decode()

def write_file(filename, content):
    if not is_probably_python(content):
        print("[!] Model output does not look like valid Python. Not writing file.")
        return False
    with open(filename, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"[+] Wrote file: {filename}")
    syn_ok, syn_msg = syntax_check(filename)
    if not syn_ok:
        print(f"[!] Syntax error in {filename}:\n{syn_msg}")
        return False
    lint_ok, lint_msg = lint_check(filename)
    if not lint_ok:
        print(f"[!] Lint warnings in {filename}:\n{lint_msg}")
    type_ok, type_msg = type_check(filename)
    if not type_ok:
        print(f"[!] Type check warnings in {filename}:\n{type_msg}")
    return True

def threaded_run(target, args=()):
    q = queue.Queue()
    def wrapper():
        res = target(*args)
        q.put(res)
    thread = threading.Thread(target=wrapper)
    thread.start()
    return thread, q

def run_file(filename):
    """Run a Python file and return stdout and stderr in a thread."""
    def _run():
        try:
            result = subprocess.run(
                ["python", filename],
                capture_output=True,
                text=True,
                timeout=60
            )
            return result.stdout, result.stderr
        except Exception as e:
            return "", str(e)
    thread, q = threaded_run(_run)
    thread.join()
    return q.get()

def fix_file(filename, error_message):
    with open(filename, "r", encoding="utf-8") as f:
        code = f.read()
    prompt = (
        f"The following code in {filename} produced this error when run:\n\n"
        f"{error_message}\n\n"
        "Here is the code:\n"
        "```\n" + code + "\n```\n"
        "Please provide a fixed version of the code. Only output the corrected code."
    )
    fixed_code = run_mixtral(prompt)
    if fixed_code.strip():
        success = write_file(filename, fixed_code)
        if success:
            print(f"[+] {filename} has been updated with the fix.")
    else:
        print("[!] Model did not return a fix.")

def main():
    print("== Robust Orchestrator ==")
    print("Type 'exit' to quit.")
    cwd = os.getcwd()
    while True:
        user = input(f"{cwd}> ").strip()
        if user.lower() in ("exit", "quit"):
            break

        if user.startswith("write "):
            try:
                if ':' not in user:
                    print("[!] Usage: write filename.py: code prompt")
                    continue
                fname, rest = user[6:].split(":", 1)
                fname = fname.strip()
                prompt = rest.strip()
                print(f"[.] Sending prompt to model...")
                code = run_mixtral(prompt)
                if not code:
                    print("[!] No code returned by model.")
                    continue
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
            print(f"[.] Running {fname} ...")
            stdout, stderr = run_file(fname)
            print("[stdout]")
            print(stdout)
            if stderr:
                print("[stderr]")
                print(stderr)
                fix = input("Error detected. Attempt to auto-fix? (y/n): ").strip().lower()
                if fix == "y":
                    fix_file(fname, stderr)
        elif user.startswith("fix "):
            fname = user[4:].strip()
            if not os.path.exists(fname):
                print("[!] File not found.")
                continue
            error = input("Paste the error message to fix: ")
            fix_file(fname, error)
        elif user.startswith("list"):
            files = os.listdir(cwd)
            for f in files:
                print(f)
        else:
            print("[.] Sending prompt to model...")
            response = run_mixtral(user)
            print(response)

if __name__ == "__main__":
    main()