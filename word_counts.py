import json
from collections import Counter
from datetime import datetime
import matplotlib.pyplot as plt
import pandas as pd
from nltk.corpus import stopwords
import nltk

# Download stopwords if not already done
nltk.download('stopwords')

# Define stopwords
stop_words = set(stopwords.words('english'))

# Load JSON data
with open("marine_record.json", "r") as file:
    json_data = json.load(file)

# Prepare data: parse dates, tokenize text, and remove stopwords
word_frequencies = []
for entry in data:
    date = datetime.strptime(entry['date'], '%Y-%m-%d')  
    words = entry['text'].lower().split()  # Basic tokenization and convert to lowercase
    filtered_words = [word for word in words if word not in stop_words]
    word_frequencies.append((date, Counter(filtered_words)))

# Aggregate data into a DataFrame
word_counts = pd.DataFrame(word_frequencies, columns=['date', 'word_counts'])

# Expand word counts into columns, summing frequencies by date
word_counts = word_counts.groupby('date')['word_counts'].apply(lambda x: sum(x, Counter())).reset_index()

# Flatten into a word-frequency DataFrame, a list of dictionaries that is easier to visualize
flattened_wordcount = []
for _, row in word_counts.iterrows():
    for word, count in row['word_counts'].items():
        flattened_wordcount.append({'date': row['date'], 'word': word, 'count': count})

#make it a panads DataFrame
wordcount_pandas = pd.DataFrame(flattened_wordcount)

#Plot top 5 words over time after removing stopwords.  Use nlargest(5) to adjust the number of words displayed on the graph.
top_words = wordcount_pandas.groupby('word')['count'].sum().nlargest(5).index
filtered_top_words = wordcount_pandas[wordcount_pandas['word'].isin(top_words)]

# Pivot for plotting
pivot_top_words = filtered_top_words.pivot(index='date', columns='word', values='count').fillna(0)

# Plot
pivot_top_words.plot(kind='line', figsize=(12, 6))
plt.title('Most Frequent Words Over Time (Excluding Stopwords)')
plt.xlabel('Date')
plt.ylabel('Frequency')
plt.legend(title='Words')
plt.grid()
plt.show()
