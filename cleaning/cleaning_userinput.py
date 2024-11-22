import json
import re

# Function to clean the text
def clean_text(text):
    # Convert to lowercase
    text = text.lower()
    # Remove line breaks and carriage returns, replacing them with a space
    text = re.sub(r'[\r\n]', ' ', text)
    # Replace multiple spaces with a single space
    text = re.sub(r' +', ' ', text)
    return text

# Prompt user for input file path
input_file = input("Enter the path to the JSON file to be cleaned: ")

# Load the JSON file
try:
    with open(input_file, 'r') as file:
        data = json.load(file)
except FileNotFoundError:
    print(f"Error: File '{input_file}' not found.")
    exit()

# Iterate over each record and clean the 'fulltext' field
for record in data:
    if 'fulltext' in record:
        record['fulltext'] = clean_text(record['fulltext'])

# Prompt user for output file name
output_file = input("Enter the name for the output file (without extension): ") + ".json"

# Save the cleaned data back to the new JSON file
with open(output_file, 'w') as file:
    json.dump(data, file, indent=4)
