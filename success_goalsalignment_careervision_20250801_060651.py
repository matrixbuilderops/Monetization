# Import json module for encoding and decoding JSON data
import json

# Define the success elements
success_elements = ["goals_alignment", "career_vision", "achievement_mindset"]

# Create a dictionary with the requested data
request_data = {"success": success_elements}

# Convert the dictionary into JSON format
json_data = json.dumps(request_data)

try:
    # Print the JSON data
    print(json_data)
except Exception as e:
    # Handle any exceptions that might occur during json.dumps()
    print(f"An error occurred: {e}")