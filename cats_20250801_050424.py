"""A simple script about cats."""
import json
# Define a dictionary of cats with their names as keys and breeds as values.
CATS = {
    "Whiskers": "Domestic Shorthair",
    "Mittens": "Siamese",
    "Tiger": "Tabby",
}
    """Print the cat dictionary in a user-friendly format."""
    print("Here is a list of our feline friends:")
        print(f"- {name.title()}: {breed.capitalize()}")
    main()
# Save the cat dictionary to a JSON file.
        json.dump(CATS, cats_file, indent=4)
    print(f"An error occurred while saving the cats data: {e}")