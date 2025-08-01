# creativity.py

def artist_block():
    """
    Helps users deal with artist's block by providing tips and exercises.
    """
    pass

def new_idea():
    """
    Generates a new, random idea for a creative project.
    """
    import random

    # Sample ideas - replace this with your own idea generator
    ideas = [
        "Create a collage using magazine clippings.",
        "Write a short story based on a random word.",
        "Design a new outfit using unconventional materials.",
        "Compose a song inspired by a dream.",
        "Illustrate a children's book."
    ]
    
    print(random.choice(ideas))

def creative_confidence():
    """
    Provides tips and exercises to boost creative confidence.
    """
    pass

if __name__ == "__main__":
    import sys

    if len(sys.argv) != 2:
        print("Usage: python creativity.py [artist_block | new_idea | creative_confidence]")
        sys.exit(1)

    requested_function = sys.argv[1].lower()

    if requested_function == "artist_block":
        artist_block()
    elif requested_function == "new_idea":
        new_idea()
    elif requested_function == "creative_confidence":
        creative_confidence()
    else:
        print(f"Unknown request: {requested_function}")
        sys.exit(1)