import json
from datetime import datetime

# Prompt the user for input and output file names
input_file = input("Enter the input JSON file path:").strip()
output_file = input("Enter the output JSON file path: ").strip()

try:
    # Load the JSON data
    with open(input_file, 'r') as file:
        json_data = json.load(file)

    # Process each entry and update the 'issue_date' field
    for entry in json_data:
        issue_date = entry["issue_date"]
        # Convert to 'YYYY-MM-DD' format
        if issue_date:
            try:
                entry["issue_date"] = datetime.strptime(issue_date, "%Y%m%d").strftime("%Y-%m-%d")
            except ValueError:
                print(f"Error: The date '{issue_date}' in entry {entry} does not match the expected format '%Y%m%d'.")

    # Save the updated JSON to the specified output file
    with open(output_file, 'w') as file:
        json.dump(json_data, file, indent=4)

except FileNotFoundError:
    print(f"Error: The file {input_file} was not found.")
except json.JSONDecodeError:
    print(f"Error: The file {input_file} does not contain valid JSON.")

