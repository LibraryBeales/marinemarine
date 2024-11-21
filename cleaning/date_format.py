import json
from datetime import datetime

# File paths
input_file = 'D:\caserepos\marinemarine\jsons\cleaned_marine_record.json'  # Input JSON file
output_file = 'D:\caserepos\marinemarine\jsons\cleaned_marine_record_date.json'  # Output JSON file

# Load the JSON data
with open(input_file, 'r') as file:
    entries = json.load(file)

# Process each entry and update the 'issue_date' field
for entry in entries:
    issue_date = entry["issue_date"]
    # Convert to 'YYYY-MM-DD' format
    entry["issue_date"] = datetime.strptime(issue_date, "%Y%m%d").strftime("%Y-%m-%d")

# Save the updated JSON to a new file
with open(output_file, 'w') as file:
    json.dump(entries, file, indent=4)
