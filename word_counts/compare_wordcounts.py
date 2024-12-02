import json
import pandas as pd
import matplotlib.pyplot as plt

review_json = "jsons/review_merged_date.json"
record_json = "jsons/record_merged_date.json"

def process_json(json_file):
    with open(json_file, "r") as file:
        json_data = json.load(file)

    json_df = pd.DataFrame(json_data)
    json_df['word_count'] = json_df['fulltext'].apply(lambda x: len(x.split()))
    json_df['issue_date'] = pd.to_datetime(json_df['issue_date'])
    json_df['year_month'] = json_df['issue_date'].dt.to_period('M')
    monthly_counts = json_df.groupby('year_month')['word_count'].sum()
    monthly_counts.index = monthly_counts.index.to_timestamp()
    return monthly_counts

monthly_counts_review = process_json(review_json)
#monthly_counts_record = process_json(record_json)

plt.figure(figsize=(14, 8))
plt.plot(monthly_counts_review.index, monthly_counts_review.values, label="Marine Review", color="blue")
#plt.plot(monthly_counts_record.index, monthly_counts_record.values, label="Marine Record", color="orange")
plt.title("Word Count Over Time - Marine Review")
plt.xlabel("Date")
plt.ylabel("Word Count")
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.show()