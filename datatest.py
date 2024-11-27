import json

# Open and parse the JSON file
with open("record_merged_date.json", "r") as file:
    data = json.load(file)  # Correctly parse JSON into Python objects

# Debug to confirm the data type and structure
print(type(data))  # Should output <class 'list'>
print(data[:2])    # Print the first two entries to inspect the structure