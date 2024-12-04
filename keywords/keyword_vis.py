import os
import pandas as pd
import matplotlib.dates as mdates
import pandas as pd
import matplotlib.pyplot as plt
from collections import Counter

csv_path = input("Enter full path to CSV file: ")

kw_df = pd.read_csv(csv_path)
kw_df['keywords'] = kw_df['keywords'].fillna("").astype(str)

keyword_counter = Counter()
for keyword_str in kw_df['keywords']:
    if keyword_str:  # Skip empty strings
        for pair in keyword_str.split(", "):
            if ": " in pair:  # Check if properly formatted
                try:
                    keyword, score = pair.split(": ")
                    keyword_counter[keyword] += float(score)
                except ValueError:
                    print(f"Skipping malformed pair: {pair}")
            else:
                print(f"Skipping improper data: {pair}")

# Get the top 10 keywords
top_keywords = keyword_counter.most_common(10)

# Plot
keywords, scores = zip(*top_keywords)
plt.figure(figsize=(10, 5))
plt.bar(keywords, scores, color='skyblue')
plt.title("Top Keywords by TF-IDF Scores")
plt.xlabel("Keywords")
plt.ylabel("Aggregate TF-IDF Score")
plt.xticks(rotation=45)

plt.savefig("kw_bar_chart.png", dpi=300, bbox_inches='tight') 
plt.close()


keyword_trends = {}

for _, row in kw_df.iterrows():
    date = row['docs_date']
    for pair in row['keywords'].split(", "):
        if ": " in pair:  
            try:
                keyword, score = pair.split(": ")
                if keyword not in keyword_trends:
                    keyword_trends[keyword] = []
                keyword_trends[keyword].append((date, float(score)))
            except ValueError:
                print(f"Skipping malformed pair: {pair}")
        else:
            print(f"Skipping improper data: {pair}")

# Filter for a few top keywords
selected_keywords = ['tonnage', 'bushels', 'packing']  #
plt.figure(figsize=(12, 6))
for keyword in selected_keywords:
    if keyword in keyword_trends:
        times, values = zip(*keyword_trends[keyword])
        plt.plot(times, values, label=keyword)

# Format the plot
plt.title("Keyword Trends Over Time")
plt.xlabel("Date")
plt.ylabel("TF-IDF Score")
plt.xticks(rotation=45)
plt.gca().xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m-%d"))
plt.gca().xaxis.set_major_locator(mdates.WeekdayLocator(interval=1))
plt.legend()
plt.savefig("kw_line_chart.png", dpi=300, bbox_inches='tight') 
plt.close()

import seaborn as sns

heatmap_data = []
dates = []

for _, row in kw_df.iterrows():
    date = row['docs_date']
    dates.append(date)
    row_data = {}
    for pair in row['keywords'].split(", "):
        if ": " in pair:  
            try:
                keyword, score = pair.split(": ")
                row_data[keyword] = float(score)
            except ValueError:
                print(f"Skipping malformed pair: {pair}")
        else:
            print(f"Skipping improper data: {pair}")

heatmap_df = pd.DataFrame(heatmap_data, index=dates).fillna(0)

# Plot the heatmap
plt.figure(figsize=(12, 6))
sns.heatmap(heatmap_df.T, cmap="Blues", annot=False)
plt.title("Keyword Importance Over Time")
plt.xlabel("Dates")
plt.ylabel("Keywords")
plt.savefig("kw_heat_map.png", dpi=300, bbox_inches='tight') 
plt.close()