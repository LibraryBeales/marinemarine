import json
from nltk.corpus import stopwords

json_file = input("Enter the path to the input JSON: ")

def count_words_excluding_stopwords(json_file, output_file):
    stop_words = set(stopwords.words('english'))
    
    with open(json_file, 'r') as file:
        data = json.load(file)  

    total_word_count = 0

    for entry in data:
        if 'fulltext' in entry:  
            text = entry['fulltext']
            words = text.split() 
            cleaned_words = [word for word in words if word.lower() not in stop_words]
            total_word_count += len(cleaned_words)
    
    with open(output_file, 'a') as file:
        file.write(f"Total words in Marine Review, excluding stopwords: {total_word_count}\n")

output_file = "word_counts/marine_reord_count.txt"  
count_words_excluding_stopwords(json_file, output_file)
