import json
import re

# Load the JSON file
with open('D:/caserepos/marinemarine/jsons/marine_record.json', 'r') as file:
    json_data = json.load(file)

def clean_text(text):
    
    text=text.lower()
    
    #remove tags - not needed, this is normally used for content scraped from web.
    #text=re.sub("</?.*?>"," <> ",text)
    
    # remove special characters and digits
    text=re.sub("(\\d|\\W)+"," ",text)
    
    # Remove line breaks and carriage returns, replacing them with a space
    text = re.sub(r'[\r\n]', ' ', text)
    # Replace multiple spaces with a single space
    text = re.sub(r' +', ' ', text)
    return text

# Iterate over each record and clean the 'fulltext' field
for record in json_data:
    if 'fulltext' in record:
        record['fulltext'] = clean_text(record['fulltext'])

# Save the cleaned data back to a new JSON file
with open('cleaned_cleanedmarine_record.json', 'w') as file:
    json.dump(json_data, file, indent=4)

