import json
import datetime
import os
import re
import traceback

ORCHESTRATOR_VERSION = "2.0.0"
PROTOCOL_CONFIG_FILE = "protocol_config.json"
SELF_TEST_FILENAME = "selftest_hello.py"
SELF_TEST_CODE = 'print("Hello, world!")'

def load_protocol_config():
    try:
        with open(PROTOCOL_CONFIG_FILE, "r", encoding="utf-8") as f:
            config = json.load(f)
        return config
    except Exception as e:
        log_error("Failed to load protocol config", exc=e)
        # Default protocol rules
        return {
            "filename_regex": r"FILENAME:\s*(\S+)",
            "code_block_regex": r"```(?:python)?\n(.*?)```",
            "max_feedback_attempts": 2
        }

def log_raw_output(output):
    with open("diagnostic_raw_output.log", "a", encoding="utf-8") as f:
        f.write(json.dumps({
            "timestamp": str(datetime.datetime.now()),
            "version": ORCHESTRATOR_VERSION,
            "raw": repr(output)
        }, indent=2) + "\n---\n")

def log_parse_result(parsed):
    with open("diagnostic_parse_log.json", "a", encoding="utf-8") as f:
        f.write(json.dumps({
            "timestamp": str(datetime.datetime.now()),
            "version": ORCHESTRATOR_VERSION,
            "parsed": parsed
        }, indent=2) + "\n---\n")

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
    # Prevent path traversal and dangerous output
    filename = filename.replace("..", "")
    filename = re.sub(r"[^a-zA-Z0-9_\-./]", "_", filename)
    return filename

def validate_input(prompt):
    # Basic validation: non-empty, safe characters
    if not prompt or not isinstance(prompt, str):
        log_error("Invalid prompt received", severity="CRITICAL")
        return False
    if len(prompt) > 10000:
        log_error("Prompt too long", severity="WARNING")
        return False
    return True

def parse_model_output(output, protocol_config, feedback_fn=None, attempt=0):
    try:
        filename_match = re.search(protocol_config["filename_regex"], output)
        code_blocks = re.findall(protocol_config["code_block_regex"], output, re.DOTALL)
        logs = re.findall(r"<LOG>(.*?)</LOG>", output, re.DOTALL)
        errors = re.findall(r"<ERROR>(.*?)</ERROR>", output, re.DOTALL)
        # Defensive checks
        if not filename_match or not code_blocks:
            log_error(
                f"Protocol violation: missing filename or code block (attempt {attempt})"
            )
            if feedback_fn and attempt < protocol_config["max_feedback_attempts"]:
                clarified = feedback_fn(output, attempt)
                return parse_model_output(clarified, protocol_config, feedback_fn, attempt + 1)
            return None  # Halt or escalate
        parsed = {
            'filename': sanitize_path(filename_match.group(1)),
            'code': code_blocks,
            'logs': logs,
            'errors': errors
        }
        log_parse_result(parsed)
        return parsed
    except Exception as e:
        log_error(f"Parse error: {e}", exc=e)
        return None

def write_file(filename, content):
    try:
        filename = sanitize_path(filename)
        folder = os.path.dirname(filename)
        if folder and not os.path.exists(folder):
            os.makedirs(folder, exist_ok=True)
            log_action(f"Created folder: {folder}")
        with open(filename, "w", encoding="utf-8") as f:
            f.write(content)
        log_action(f"Wrote file: {filename}")
    except Exception as e:
        log_error(f"File write error: {filename}: {e}", exc=e)

def self_test_heartbeat():
    # Regularly test basic workflow
    try:
        write_file(SELF_TEST_FILENAME, SELF_TEST_CODE)
        result = os.system(f"python {SELF_TEST_FILENAME}")
        log_action(f"Self-test heartbeat result: {result}")
        if result != 0:
            log_error("Self-test failed", severity="CRITICAL")
            return False
        return True
    except Exception as e:
        log_error("Self-test exception", exc=e)
        return False

def orchestrate(prompt, model_fn, feedback_fn):
    protocol_config = load_protocol_config()
    if not validate_input(prompt):
        return
    output = model_fn(prompt)
    log_raw_output(output)
    parsed = parse_model_output(output, protocol_config, feedback_fn)
    if parsed:
        write_file(parsed['filename'], parsed['code'][0])
        log_action(f"Orchestration complete for: {parsed['filename']}")
    else:
        log_error("Orchestration failed: could not parse model output", severity="CRITICAL")

# Example feedback function
def feedback_fn(output, attempt):
    # You would replace this stub with logic to re-prompt the model for clarification
    log_action(f"Requesting clarification from model (attempt {attempt+1})")
    # Example: append "Please format output according to protocol."
    return output + "\nPlease format output according to protocol."

# Example model function stub
def model_fn(prompt):
    # Replace with actual model call
    return f'FILENAME: hello.py\n```python\nprint("Hello, world!")\n```'

# Example usage
if __name__ == "__main__":
    orchestrate("Generate hello world script in Python", model_fn, feedback_fn)
    self_test_heartbeat()