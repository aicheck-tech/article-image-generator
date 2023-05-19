import json
from pathlib import Path
import logging

logging.getLogger().setLevel(logging.INFO)
DIRECTORY_PATH = Path(__file__).parent / "storage/datasets/default/"
OUTPUT_PATH = Path(__file__).parent / "merged.json"


def merge_json_files():
    # Create an empty list to store the JSON data
    json_data = []

    # Iterate over all JSON files in the specified directory
    for file_path in DIRECTORY_PATH.rglob('*.json'):
        # Read the JSON file
        with open(file_path, 'r', encoding="utf-8") as file:
            try:
                # Load the JSON data
                data = json.load(file)

                # Append the data to the list
                json_data.append(data)
            except json.JSONDecodeError:
                print(f"Error: Failed to parse JSON in file {file_path}")

    # Create a dictionary with keys starting from 0
    with open(OUTPUT_PATH, 'w', encoding="utf-8") as file:
        file.write(json.dumps(json_data, indent=4))


# Print the resulting dictionary
if __name__ == "__main__":
    logging.info("Merging JSON files...")
    print(merge_json_files())
    logging.info("Done!")
