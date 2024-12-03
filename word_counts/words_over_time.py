import json
from datetime import datetime
import matplotlib.pyplot as plt
from collections import defaultdict, Counter

json_file = input("Enter the file path: ")

with open(json_file, "r") as file:
    json_data = json.load(file)

user_input = input("Enter the words to visualize, separated by commas: ")
selected_words = {word.strip().lower() for word in user_input.split(",")}

# Initialize a dictionary to store word counts by date
word_counts_by_date = defaultdict(Counter)

# Process data and count only the selected words
for entry in json_data:
    try:
        date = datetime.strptime(entry['issue_date'], '%Y-%m-%d')  # Parse date
        words = entry['fulltext'].split()  # Tokenize fulltext
        for word in words:
            if word in selected_words:  # Check if word is in user-specified list
                word_counts_by_date[date][word] += 1
    except KeyError as e:
        print(f"Skipping invalid entry: {entry} - Missing key: {e}")
        continue

# Convert to a DataFrame for easier plotting
import pandas as pd

# Flatten the word counts into a list of dictionaries
flattened_wordcount = [
    {'date': date, 'word': word, 'count': count}
    for date, counts in word_counts_by_date.items()
    for word, count in counts.items()
]

wordcount_df = pd.DataFrame(flattened_wordcount)

# Pivot the data for plotting
pivot_selected_words = wordcount_df.pivot(index='date', columns='word', values='count').fillna(0)

#set a rolling average window to smooth the curves.  30 = monthly 7 = weekly, etc.
smoothing_selected_words = pivot_selected_words.rolling(window=30, min_periods=1).mean()

# Plot the data
if not smoothing_selected_words.empty:
    smoothing_selected_words.plot(kind='line', figsize=(12, 6))
    plt.title('Selected Word Frequencies Over Time')
    plt.xlabel('Date')
    plt.ylabel('Frequency')
    plt.legend(title='Words')
    plt.grid()
    plt.show()
else:
    print("No matching words found.")