# productivity_script.py

import os
import sys
import json
from typing import List

def read_request_file(file_path: str) -> dict:
    """Reads JSON request file and returns its content as a Python dictionary.

    Args:
      file_path (str): Path to the request JSON file.

    Returns:
      dict: Request data in the form of a Python dictionary.
    """
    try:
        with open(file_path, 'r') as file:
            return json.load(file)
    except Exception as e:
        print(f"Error reading request file: {e}", file=sys.stderr)
        sys.exit(1)

def handle_imposter_syndrome(topic: str) -> None:
    """Handles imposter syndrome topic by printing a motivational message.

    Args:
      topic (str): The requested topic ("imposter_syndrome").
    """
    print("You've got this! Remember, everyone feels like an imposter sometimes.")

def handle_burnout(topic: str) -> None:
    """Handles burnout topic by suggesting a break and self-care.

    Args:
      topic (str): The requested topic ("burnout").
    """
    print("It's time to take a break and focus on self-care. You can't pour from an empty cup.")

def handle_workspace_focus(topic: str) -> None:
    """Handles workspace focus topic by suggesting tips for improving focus.

    Args:
      topic (str): The requested topic ("workspace_focus").
    """
    print("Consider decluttering your workspace, using nature sounds as background noise, and taking regular short breaks.")

def handle_topic(topic: str) -> None:
    """Handles a specific productivity topic.

    Args:
      topic (str): The requested productivity topic.
    """
    if topic == "imposter_syndrome":
        handle_imposter_syndrome(topic)
    elif topic == "burnout":
        handle_burnout(topic)