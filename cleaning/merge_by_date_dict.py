#Creates a dictionary of dates (key) and the merged fulltext (value) published on that date
from collections import defaultdict
import json

with open('D:\caserepos\marinemarine\jsons\marine_record.json', 'r') as file:
    data = json.load(file)

# Group by issue_date
grouped_text = defaultdict(list)

for entry in data:
    grouped_text[entry['issue_date']].append(entry['fulltext'])

# Join fulltext fields for each date
result = {
    issue_date: f'"{" ".join(fulltexts)}"'
    for issue_date, fulltexts in grouped_text.items()
}

# Print the result
print(json.dumps(result, indent=4))


'''
This old script doesn't use defaultdict, so you have to check for the key in the dictionary before adding the fulltext each time. 

# Initialize an empty dictionary

with open('D:\caserepos\marinemarine\jsons\marine_record.json', 'r') as file:
    data = json.load(file)
    
grouped_text = {}

# Iterate through the list of entries
for entry in data:
    issue_date = entry['issue_date']  # Extract the issue_date
    fulltext = entry['fulltext']  # Extract the fulltext
    
    # Check if the issue_date already exists in the dictionary
    if issue_date not in grouped_text:
        grouped_text[issue_date] = []  # Initialize an empty list if the key doesn't exist
    
    # Append the fulltext to the list for that issue_date
    grouped_text[issue_date].append(fulltext)

# Join and format the fulltext fields for each date
result = {
    issue_date: f'"{" ".join(fulltexts)}"'
    for issue_date, fulltexts in grouped_text.items()
}

# Print the result
print(json.dumps(result, indent=4))
'''
