from bertopic import BERTopic
from sklearn.feature_extraction.text import CountVectorizer
from sentence_transformers import SentenceTransformer
import json
import pandas as pd
import nltk  #
from nltk.corpus import stopwords  #did this with no stopwords first....  Classic...
 
json_file = input("Enter the file path: ")
with open(json_file, "r") as file:
    json_data = json.load(file)

nltk.download("stopwords")
stop_words = list(stopwords.words("english")) #must be list

documents = [entry['fulltext'] for entry in json_data]
vectorizer = CountVectorizer(stop_words=stop_words)
embedding_model = SentenceTransformer("all-MiniLM-L6-v2")  # picked a lightweight mnodel, not an effective model...
topic_model = BERTopic(embedding_model=embedding_model, vectorizer_model=vectorizer, language="english")
topics, probs = topic_model.fit_transform(documents)
print("Topics:")
topic_info = topic_model.get_topic_info()
for idx, topic_name in enumerate(topic_info['Name'][1:]):  #excludes outiers?
    print(f"Topic {idx}: {topic_name}")

with open("topic_modeling/bertopic_topics.txt", "w") as file:
    file.write("Topics:\n")
    for _, row in topic_info.iterrows():
        file.write(f"Topic {row['Topic']}: {row['Name']}\n\n")

print("Topics saved to 'topic_modeling/bertopic_topics.txt'")

visualization = topic_model.visualize_topics()
visualization.write_html("topic_modeling/bertopic_topics.html")
print("Vis saved to 'bertopic_topics.html'")

visualization.show()


#reduced_topic_model = topic_model.reduce_topics(documents, nr_topics=10)
