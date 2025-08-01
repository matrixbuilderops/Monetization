# stress_relief.py

def deep_breathing():
    """Help user to relax by deep breathing exercise."""
    print("Take a slow, deep breath in through your nose.")
    print("Hold it for a moment.")
    print("Now exhale slowly through your mouth.")
    print("Repeat this process for several minutes.")
    
def tension_release():
    """Guide user to release physical tension."""
    print("Tense the muscles in your feet and toes")
    print("Hold for a count of 10.")
    print("Relax your feet and toes.")
    print("Work your way up through your body, tensing and releasing each muscle group.")
    
def deadline_pressure():
    """Provide tips to manage deadline pressure."""
    print("Break down large tasks into smaller, manageable parts.")
    print("Create a detailed plan with deadlines for each part.")
    print("Prioritize and focus on the most critical tasks.")
    print("Take regular breaks to avoid burnout.")
    
def main():
    # Request: "stress_relief": ["deep_breathing", "tension_release", "deadline_pressure"]
    requested_activities = ["deep_breathing", "tension_release", "deadline_pressure"]
    
    for activity in requested_activities:
        if activity == "deep_breathing":
            deep_breathing()
        elif activity == "tension_release":
            tension_release()
        elif activity == "deadline_pressure":
            deadline_pressure()
        else:
            print(f"{activity} is not a valid stress relief technique.")
    
if __name__ == "__main__":
    main()