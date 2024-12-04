import pandas as pd
import json

json_file = input("Enter the path to JSON file: ")
json_data = pd.read_json(json_file, lines=True)

sorted_data = json_data.sort_values(by='polarity', ascending=True)

lowest_sent = sorted_data.head(10)

output_file = input("Enter name of output file: ")
if not output_file.endswith('.json'):
    output_file += '.json'

lowest_sent.to_json(output_file, orient='records', lines=True)

print(f"Ten lowest sentiment entries saved to {output_file}")
