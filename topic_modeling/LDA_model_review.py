

import json
import pandas as pd
from gensim.models import LdaModel
from gensim.corpora import Dictionary
from nltk.corpus import stopwords
import nltk
import matplotlib.pyplot as plt
import re
import pyLDAvis
import pyLDAvis.gensim_models

json_file = input("Enter the file path: ")

with open(json_file, "r") as file:
    json_data = json.load(file)

documents = [entry['fulltext'] for entry in json_data]

nltk.download('stopwords')
stop_words = set(stopwords.words('english'))

def preprocess_text(text):
    text = re.sub(r'\W+', ' ', text.lower()) 
    tokens = [word for word in text.split() if word not in stop_words and len(word) > 2]    
    return tokens

processed_texts = [preprocess_text(doc) for doc in documents]
dictionary = Dictionary(processed_texts)
corpus = [dictionary.doc2bow(text) for text in processed_texts]

lda_model = LdaModel(corpus, num_topics=6, id2word=dictionary, passes=20, random_state=42)

topics = lda_model.print_topics(num_words=12)
print("Topics:")
for idx, topic in topics:
    print(f"Topic {idx}: {topic}")

with open("topic_modeling/topics.txt", "w") as file:
    file.write("Extracted Topics:\n")
    for idx, topic in topics:
        file.write(f"Topic {idx}:\n{topic}\n\n")

print("Saved to 'topic_modeling/topics.txt'")


lda_vis = pyLDAvis.gensim_models.prepare(lda_model, corpus, dictionary)
pyLDAvis.display(lda_vis)
pyLDAvis.save_html(lda_vis, 'lda_vis.html')
print("Saved to 'lda_vis.html'")


'''
  File "strptime.pyx", line 534, in pandas._libs.tslibs.strptime.array_strptime
  File "strptime.pyx", line 355, in pandas._libs.tslibs.strptime.array_strptime
ValueError: time data "1891-01-01" doesn't match format "%Y%m%d", at position 0. You might want to try:
    - passing `format` if your strings have a consistent format;
    - passing `format='ISO8601'` if your strings are all ISO8601 but not necessarily in exactly the same format;
    - passing `format='mixed'`, and the format will be inferred for each element individually. You might want to use `dayfirst` alongside this.
'''