import json
import pandas as pd
import matplotlib.pyplot as plt
import re

json_file = input("Enter the file path: ")

# Load JSON data
with open(json_file, "r") as file:
    json_data = json.load(file)

json_data = pd.DataFrame(json_data)

json_data['word_count'] = json_data['fulltext'].apply(lambda x: len(x.split()))

json_data['issue_date'] = pd.to_datetime(json_data['issue_date'])
json_data_grouped = json_data.groupby('issue_date')['word_count'].sum().reset_index()

plt.figure(figsize=(14, 8))
plt.plot(json_data_grouped['issue_date'], json_data_grouped['word_count'], label="Word Count")
plt.title("Word Count Over Time, Marine Review")
plt.xlabel("Date")
plt.ylabel("Count")
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.show()
