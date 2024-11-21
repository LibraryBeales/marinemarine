import json

# Ask the user for the input file name
input_file = input("Enter the name of the input JSON file (e.g., data.json): ")

# Read the input file
try:
    with open(input_file, "r") as f:
        data = json.load(f)
except FileNotFoundError:
    print(f"Error: The file '{input_file}' was not found.")
    exit(1)
except json.JSONDecodeError:
    print(f"Error: The file '{input_file}' is not a valid JSON file.")
    exit(1)

# Group by issue_date
grouped_text = {}

for entry in data:
    issue_date = entry['issue_date']
    fulltext = entry['fulltext']
    
    if issue_date not in grouped_text:
        grouped_text[issue_date] = {
            "issue_date": issue_date,
            "fulltext": fulltext  # Start with the first fulltext
        }
    else:
        # Append the new fulltext to the existing one, separated by a space
        grouped_text[issue_date]["fulltext"] += f" {fulltext}"

# Create a list from the grouped data
merged_data = list(grouped_text.values())

# Ask the user for the output file name
output_file = input("Enter the name of the output JSON file (e.g., merged_issues.json): ")

# Save to the output JSON file
try:
    with open(output_file, "w") as f:
        json.dump(merged_data, f, indent=4)
    print(f"Merged JSON saved to {output_file}")
except Exception as e:
    print(f"Error: Could not save the file '{output_file}'. Reason: {e}")