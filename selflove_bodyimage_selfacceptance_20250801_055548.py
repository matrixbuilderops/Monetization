# self_love_program.py

import json

def get_self_love_topics():
    """
    Returns a list of topics related to self love.
    """
    return ["body_image", "self_acceptance", "personal_growth"]

if __name__ == "__main__":
    try:
        requested_topic = "self_love"
        if requested_topic not in LOVE_TOPICS:
            print(f"Error: Topic '{requested_topic}' not supported.")
            print("Supported topics are:")
            for topic in LOVE_TOPICS:
                print(f"- {topic}")
        else:
            self_love_topics = get_self_love_topics()
            print(f"Self Love Topics: {json.dumps(self_love_topics)}")
    except Exception as e:
        print(f"Error: {e}")