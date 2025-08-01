import subprocess
import os
import threading
import time
import sys

def run_mixtral(prompt):
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
        # Send prompt, close stdin to signal EOF
        process.stdin.write(prompt + "\n")
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
    with open(filename, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"[+] Wrote file: {filename}")

def run_file(filename):
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

def main():
    print("== Conversational Orchestrator ==")
    print("Type 'exit' to quit. Type 'run filename.py' or 'write filename.py: code prompt' or just chat with the model.")
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
                code = run_mixtral(prompt)
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
            files = os.listdir(cwd)
            for f in files:
                print(f)
        else:
            # Chat with the model as default!
            response = run_mixtral(user)
            print(response)

if __name__ == "__main__":
    main()