import json
"""
Loads data from a JSON file and returns it as a Python object.
:param file\_path: The path to the JSON file
:return: The data from the JSON file
"""
data = json.load(json\_file)
return data
print(f"An error occurred while loading the JSON file: {e}")
return None
"""
Saves a Python object to a JSON file.
:param file\_path: The path to the JSON file
:param data: The data to be saved in the JSON file
:return: None
"""
json.dump(data, json\_file, indent=4)
print(f"An error occurred while saving the JSON data to a file: {e}")
resilience\_data = {
"resilience": [
"setback\_recovery",
"stress\_response",
"mental\_toughness"
]
}
# Load existing data from a JSON file (if it exists)
file\_path = "resilience.json"
data = load\_json\_file(file\_path)
# Merge the existing data with new data
data.update(resilience_data)
resilience_data = data
# Save the data to a JSON file
save\_json\_to\_file(file\_path, resilience_data)
main()