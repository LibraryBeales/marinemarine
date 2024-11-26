import json
from collections import Counter
from datetime import datetime
import matplotlib.pyplot as plt
import pandas as pd
from nltk.corpus import stopwords
import nltk

#THIS WHOLE THING IS BACKWARDS...  Generates a memory error....  WHY DID I COUNT ALL THE WORDS BEFORE SELECTING THE WORDS I WANT TO SEE VISUALIZED?.....  Maybe enter the words you want counted first.....

# Download stopwords if not already done
nltk.download('stopwords')

# Define stopwords
stop_words = set(stopwords.words('english'))

json_file = input("Enter the file path: ")

# Load JSON data
with open(json_file, "r") as file:
    json_data = json.load(file)

# Prepare data: parse dates, tokenize text, and remove stopwords
word_frequencies = []
for entry in json_data:
    date = datetime.strptime(entry['issue_date'], '%Y-%m-%d')  # Adjust format if needed
    words = entry['fulltext'].split()  # Basic tokenization and convert to lowercase  removed .lower() because that was done during cleaning...
    filtered_words = [word for word in words if word not in stop_words]
    word_frequencies.append((date, Counter(filtered_words)))

# Aggregate data into a DataFrame
df = pd.DataFrame(word_frequencies, columns=['date', 'word_counts'])

# Expand word counts into columns, summing frequencies by date
df = df.groupby('date')['word_counts'].apply(lambda x: sum(x, Counter())).reset_index()

# Flatten into a word-frequency DataFrame
flattened_wordcount = []
for _, row in df.iterrows():
    for word, count in row['word_counts'].items():
        flattened_wordcount.append({'date': row['date'], 'word': word, 'count': count})

#make it a panads DataFrame
freq_df = pd.DataFrame(flattened_wordcount)

# Ask the user for specific words to plot
words_input = input("Enter the words you want to plot, separated by commas: ")
selected_words = [word.strip().lower() for word in words_input.split(",")]

# Filter the DataFrame for the selected words
filtered_selected_words = freq_df[freq_df['word'].isin(selected_words)]

# Pivot for plotting
pivot_selected_words = filtered_selected_words.pivot(index='issue_date', columns='word', values='count').fillna(0)

# Plot
if not pivot_selected_words.empty:
    pivot_selected_words.plot(kind='line', figsize=(12, 6))
    plt.title('Selected Word Frequencies Over Time')
    plt.xlabel('Date')
    plt.ylabel('Frequency')
    plt.legend(title='Words')
    plt.grid()
    plt.show()
else:
    print("None of the selected words are present in the data.")
