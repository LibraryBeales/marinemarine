#hold!
'''
Start with a sentiment graph 
over time to see if there is an interesting correleation 
between sentiment and global/regional/local events. 

Pattern package has opinion and fact detection- subjectivity over time
Locate local resources to share this with and interpret visualizations, starting with Walter Lewis.
As with all the other ML things here, I will ahve to spend some time training...

'''

import pandas as pd
from pattern.en import sentiment
import matplotlib.pyplot as plt
import json

json_file = input("Enter the file path: ")
with open(json_file, "r") as file:
    json_data = json.load(file)

#error checking for json 
if 'issue_date' not in json_data or 'fulltext' not in json_data:
    raise ValueError("No 'issue_date' and/or 'fulltext' fields.")

json_data['issue_date'] = pd.to_datetime(json_data['issue_date'])

def analyze_sentiment(text):
    polarity, subjectivity = sentiment(text)
    return pd.Series({'polarity': polarity, 'subjectivity': subjectivity})

json_data[['polarity', 'subjectivity']] = json_data['fulltext'].apply(analyze_sentiment)

json_data['is_fact'] = json_data['subjectivity'] < 0.5  # default threshold? subjectivity < 0.5 = fact
json_data['is_opinion'] = json_data['subjectivity'] >= 0.5

json_data['month'] = json_data['issue_date'].dt.to_period('M')
monthly_data = json_data.groupby('month').agg(
    avg_polarity=('polarity', 'mean'),
    avg_subjectivity=('subjectivity', 'mean'),
    fact_ratio=('is_fact', 'mean'),  
    opinion_ratio=('is_opinion', 'mean')  
).reset_index()

# 
monthly_data['month'] = monthly_data['month'].dt.to_timestamp()


plt.figure(figsize=(14, 8))

plt.subplot(3, 1, 1)
plt.plot(monthly_data['month'], monthly_data['avg_polarity'], marker='o', color='blue')
plt.title('Monthly Average Polarity')
plt.ylabel('Polarity')
plt.grid(True)

plt.subplot(3, 1, 2)
plt.plot(monthly_data['month'], monthly_data['avg_subjectivity'], marker='o', color='orange')
plt.title('Monthly Average Subjectivity')
plt.ylabel('Subjectivity')
plt.grid(True)

plt.subplot(3, 1, 3)
plt.plot(monthly_data['month'], monthly_data['fact_ratio'], label='Fact Ratio', marker='o', color='green')
plt.plot(monthly_data['month'], monthly_data['opinion_ratio'], label='Opinion Ratio', marker='o', color='red')
plt.title('Fact and Opinion')
plt.ylabel('Ratio')
plt.legend()
plt.grid(True)

plt.tight_layout()
plt.show()