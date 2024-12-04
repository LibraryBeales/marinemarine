import pandas as pd
import json

json_file = input("Enter the path to the JSON file: ")
json_data = pd.read_json(json_file, lines=True)

# Find the minimum polarity value
min_polarity = json_data['polarity'].min()

# Filter rows where polarity equals the minimum value
lowest_sent = json_data[json_data['polarity'] == min_polarity]

# Save the filtered entries to a new JSON file
output_file = input("Enter the name of the output : ")
if not output_file.endswith('.json'):
    output_file += '.json'

lowest_sent.to_json(output_file, orient='records', lines=True)

print(f"Saved to {output_file}")
