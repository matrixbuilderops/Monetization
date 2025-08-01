# gratitude.py

def daily_practice():
    """A simple description of the gratitude practice that could be done on a daily basis."""
    print("Gratitude daily practice: Reflect on three new things you are grateful for today.")

def gratitude_after_loss():
    """A description of how expressing gratitude can help after a loss."""
    print("Gratitude after loss: Though it may be difficult, try to find something to be grateful for in this experience. It can help you move forward with more resilience.")

def gratitude_for_body():
    """A description of how practicing gratitude for your body can improve self-image."""
    print("Gratitude for body: Take a moment to appreciate your body for all it does for you. This practice can lead to improved self-image and higher self-esteem.")

def main():
    gratitude_topics = ["daily_practice", "gratitude_after_loss", "gratitude_for_body"]
    
    if not all(topic in locals() for topic in gratitude_topics):
        print("One or more gratitude topics are missing. Please make sure they are all defined.")
        return
    
    while True:
        user_input = input("\nWhich gratitude topic would you like to explore? (enter 'q' to quit): ").lower()
        
        if user_input == "q":
            break
        
        elif user_input in gratitude_topics:
            globals()[user_input]()
        else:
            print(f"Sorry, '{user_input}' is not a valid topic. Please try again.")

if __name__ == "__main__":
    main()