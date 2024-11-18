import json
import re

# Load the JSON file
with open('marine_record.json', 'r') as file:
    data = json.load(file)

# Function to clean the text
def clean_text(text):
    # Convert to lowercase
    text = text.lower()
    # Remove line breaks and carriage returns, replacing them with a space
    text = re.sub(r'[\r\n]', ' ', text)
    # Replace multiple spaces with a single space
    text = re.sub(r' +', ' ', text)
    return text

# Iterate over each record and clean the 'fulltext' field
for record in data:
    if 'fulltext' in record:
        record['fulltext'] = clean_text(record['fulltext'])

# Save the cleaned data back to a new JSON file
with open('cleaned_marine_record.json', 'w') as file:
    json.dump(data, file, indent=4)

print("Cleaning complete. The output is saved in 'cleaned_marine_record.json'.")
