import json
import pandas as pd

review_json = "jsons/review_merged_date.json"
with open(review_json, 'r') as file:
    json_data = json.load(file)

json_df = pd.DataFrame(json_data)

json_df['word_count'] = json_df['fulltext'].apply(lambda x: len(x.split()))

json_df['issue_date'] = pd.to_datetime(json_df['issue_date'])

word_count_table = json_df[['issue_date', 'word_count']]

pd.set_option('display.max_rows', None)  # Show all rows
pd.set_option('display.max_columns', None)  # Show all columns
pd.set_option('display.width', None)  # Avoid line wrapping
pd.set_option('display.max_colwidth', None)  # Avoid column truncation


print(word_count_table)