# Mindfulness Python Script
# Based on the request: {"mindfulness": ["present_awareness", "grounding", "calm_presence"]}

import json

def present_awareness():
    """Present Awareness practice."""
    print("Focus on the current moment and your present experiences.")

def grounding():
    """Grounding exercise to connect with reality."""
    print("Engage your senses to connect with the physical world around you.")

def calm_presence():
    """Cultivate a calm presence."""
    print("Develop a serene and tranquil state of being.")

if __name__ == "__main__":
    # Request data as dictionary
    request_data = {
        "mindfulness": [
            "present_awareness",
            "grounding",
            "calm_presence"
        ]
    }

    try:
        # Extract mindfulness practices from the request data
        requested_practices = request_data["mindfulness"]

        # Perform each mindfulness practice
        for practice in requested_practices:
            if practice == "present_awareness":
                present_awareness()
            elif practice == "grounding":