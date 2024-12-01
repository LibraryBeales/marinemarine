import json
import pandas as pd
from gensim.models import LdaModel
from gensim.corpora import Dictionary
from nltk.corpus import stopwords
import nltk
import matplotlib.pyplot as plt
import re

json_file = input("Enter the file path: ")

with open(json_file, "r") as file:
    json_data = json.load(file)

fulltexts = [entry['fulltext'] for entry in json_data]
dates = [entry['issue_date'] for entry in json_data]

nltk.download('stopwords')
stop_words = set(stopwords.words('english'))

def preprocess_text(text):
    text = re.sub(r'\W+', ' ', text.lower())
    tokens = [word for word in text.split() if word not in stop_words and len(word) > 2]    
    return tokens

processed_texts = [preprocess_text(text) for text in fulltexts]

dictionary = Dictionary(processed_texts)
corpus = [dictionary.doc2bow(text) for text in processed_texts]

num_topics = 6
lda_model = LdaModel(corpus, num_topics=num_topics, id2word=dictionary, passes=10)

topics = lda_model.print_topics(num_words=12)
print("Top Topics:")
for idx, topic in topics:
    print(f"Topic {idx}: {topic}")

with open("topics.txt", "w") as file:
    file.write("Extracted Topics:\n")
    for idx, topic in topics:
        file.write(f"Topic {idx}:\n{topic}\n\n")

print("Topics saved to 'topics.txt'")

topic_distributions = [lda_model.get_document_topics(doc, minimum_probability=0) for doc in corpus]

topic_df = pd.DataFrame([
    {'date': dates[i], 'topic': topic, 'probability': prob}
    for i, doc_topics in enumerate(topic_distributions)
    for topic, prob in doc_topics
])

topic_df['date'] = pd.to_datetime(topic_df['date'], format='%Y%m%d')

topic_df['year'] = topic_df['date'].dt.year
prevalence = topic_df.groupby(['year', 'topic'])['probability'].mean().unstack(fill_value=0)

prevalence.plot(kind='line', figsize=(14, 8), colormap='tab10')
plt.title('Topics Over Time')
plt.xlabel('Year')
plt.ylabel('Average Topic Probability')
plt.legend(title='Topics', loc='upper left')#This is a fairly useles legend, need some way to name the topics before visualization...
plt.show()

'''
  File "strptime.pyx", line 534, in pandas._libs.tslibs.strptime.array_strptime
  File "strptime.pyx", line 355, in pandas._libs.tslibs.strptime.array_strptime
ValueError: time data "1891-01-01" doesn't match format "%Y%m%d", at position 0. You might want to try:
    - passing `format` if your strings have a consistent format;
    - passing `format='ISO8601'` if your strings are all ISO8601 but not necessarily in exactly the same format;
    - passing `format='mixed'`, and the format will be inferred for each element individually. You might want to use `dayfirst` alongside this.
'''