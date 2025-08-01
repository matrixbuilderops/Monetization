import subprocess
import os
import shlex

def run_mixtral(prompt):
    """Send prompt to Mixtral model via Ollama and return response."""
    cmd = "ollama run mixtral:8x7b-instruct-v0.1-q6_K"
    process = subprocess.Popen(
        shlex.split(cmd),
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    out, err = process.communicate(prompt)
    if err:
        return out.strip() + "\n[stderr: " + err.strip() + "]"
    return out.strip()

def write_file(filename, content):
    """Write content to filename."""
    with open(filename, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"[+] Wrote file: {filename}")

def run_file(filename):
    """Run a Python file and return stdout and stderr."""
    try:
        result = subprocess.run(
            ["python", filename],
            capture_output=True,
            text=True,
            timeout=60
        )
        print("[stdout]")
        print(result.stdout)
        if result.stderr:
            print("[stderr]")
            print(result.stderr)
        return result.stdout, result.stderr
    except Exception as e:
        print(f"[!] Error running file: {e}")
        return "", str(e)

def fix_file(filename, error_message):
    """Ask Mixtral to fix the file based on error message."""
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
        write_file(filename, fixed_code)
        print(f"[+] {filename} has been updated with the fix.")
    else:
        print("[!] Model did not return a fix.")

def main():
    print("== Local Orchestrator Agent ==")
    print("Type 'exit' to quit.")
    cwd = os.getcwd()
    while True:
        user = input(f"{cwd}> ").strip()
        if user.lower() in ("exit", "quit"):
            break

        if user.startswith("write "):
            # write my_script.py: Make a Python script that prints Hello
            try:
                fname, rest = user[6:].split(":", 1)
                prompt = rest.strip()
                code = run_mixtral(prompt)
                write_file(fname.strip(), code)
            except Exception as e:
                print(f"[!] Write error: {e}")
        elif user.startswith("show "):
            # show my_script.py
            fname = user[5:].strip()
            if os.path.exists(fname):
                with open(fname, 'r', encoding='utf-8') as f:
                    print(f.read())
            else:
                print("[!] File not found.")
        elif user.startswith("run "):
            # run my_script.py
            fname = user[4:].strip()
            if not os.path.exists(fname):
                print("[!] File not found.")
                continue
            stdout, stderr = run_file(fname)
            # Auto-fix on error
            if stderr:
                fix = input("Error detected. Attempt to auto-fix? (y/n): ").strip().lower()
                if fix == "y":
                    fix_file(fname, stderr)
        elif user.startswith("fix "):
            # fix my_script.py
            fname = user[4:].strip()
            if not os.path.exists(fname):
                print("[!] File not found.")
                continue
            error = input("Paste the error message to fix: ")
            fix_file(fname, error)
        elif user.startswith("list"):
            # list files
            files = os.listdir(cwd)
            for f in files:
                print(f)
        else:
            # Default: send prompt to model, print response
            print(run_mixtral(user))

if __name__ == "__main__":
    main()