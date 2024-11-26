import json
from datetime import datetime
import matplotlib.pyplot as plt
from collections import defaultdict, Counter

json_file = input("Enter the file path: ")

# Load JSON data
with open(json_file, "r") as file:
    json_data = json.load(file)


# Get user input for words of interest
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
flattened_data = [
    {'date': date, 'word': word, 'count': count}
    for date, counts in word_counts_by_date.items()
    for word, count in counts.items()
]

# Create a DataFrame
freq_df = pd.DataFrame(flattened_data)

# Pivot the data for plotting
pivot_df = freq_df.pivot(index='date', columns='word', values='count').fillna(0)

# Plot the data
if not pivot_df.empty:
    pivot_df.plot(kind='line', figsize=(12, 6))
    plt.title('Selected Word Frequencies Over Time')
    plt.xlabel('Date')
    plt.ylabel('Frequency')
    plt.legend(title='Words')
    plt.grid()
    plt.show()
else:
    print("No matching words found.")