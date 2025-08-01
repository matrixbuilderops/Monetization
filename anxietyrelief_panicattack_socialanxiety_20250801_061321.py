# anxiety\_relief.py

import json

def handle_panic_attack():
    """Handle panic attack related tasks."""
    print("Handling panic attack...")

def handle_social_anxiety():
    """Handle social anxiety related tasks."""
    print("Helping with social anxiety...")

def handle_future_worry():
    """Handle future worry related tasks."""
    print("Alleviating concerns about the future...")

def main():
    try:
        anxiety_request = {
            "anxiety_relief": [
                "panic_attack",
                "social_anxiety",
                "future_worry"
            ]
        }

        for item in anxiety_request["anxiety_relief"]:
            if item == "panic_attack":
                handle_panic_attack()
            elif item == "social_anxiety":
                handle_social_anxiety()
            elif item == "future_worry":
                handle_future_worry()
            else:
                raise ValueError(f"Unknown anxiety type: {item}")

    except KeyError as e:
        print(f"Missing key in request: {e}")
    except TypeError as e:
        print("Invalid request format:", e)
    except ValueError as e:
        print(e)

if __name__ == "__main__":
    main()