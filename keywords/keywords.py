import pandas as pd
import json

json_file = input("Enter the file path: ")
with open(json_file, "r") as file:
    json_data = json.load(file)

json_data = pd.DataFrame(json_data)
print("Schema:\n\n",json_data.dtypes)
print("Number of questions,columns=",json_data.shape)

import re
def pre_process(text):
    
    # lowercase
    text=text.lower()
    
    #remove tags
    text=re.sub("</?.*?>"," <> ",text)
    
    # remove special characters and digits
    text=re.sub("(\\d|\\W)+"," ",text)
    
    return text

df_idf['text'] = df_idf['title'] + df_idf['body']
df_idf['text'] = df_idf['text'].apply(lambda x:pre_process(x))

#show the first 'text'
df_idf['text'][2]