#hold!
'''
Start with a sentiment graph 
over time to see if there is an interesting correleation 
between sentiment and global/regional/local events. 

Pattern package has opinion and fact detection- subjectivity over time
Locate local resources to share this with and interpret visualizations, starting with Walter Lewis.
As with all the other ML things here, I will ahve to spend some time training...

Identify candidates for filtering date ranges to see more detailed cahnges.
MOdify subjectivity threshold due to businesslike content of the corpus

'''

import pandas as pd
from pattern3.text.en import sentiment
import matplotlib.pyplot as plt
import json

json_file = input("Enter the file path: ")
with open(json_file, "r") as file:
    json_data = json.load(file)

json_data = pd.DataFrame(json_data)

print(json_data.head()) 
print(json_data.columns)  

if json_data['issue_date'].isnull().all() or json_data['fulltext'].isnull().all():
    raise ValueError("The 'issue_date' or 'fulltext' columns are empty.")

print(json_data['issue_date'].isnull().sum())  
print(json_data['fulltext'].isnull().sum()) 

json_data['issue_date'] = pd.to_datetime(json_data['issue_date'], errors='coerce')
print(json_data['issue_date'].head())

#error checking for json 
#if 'issue_date' not in json_data or 'fulltext' not in json_data:
    #raise ValueError("No 'issue_date' and/or 'fulltext' fields.")

json_data['issue_date'] = pd.to_datetime(json_data['issue_date'])

def analyze_sentiment(text):
    polarity, subjectivity = sentiment(text)
    return pd.Series({'polarity': polarity, 'subjectivity': subjectivity})

json_data[['polarity', 'subjectivity']] = json_data['fulltext'].apply(analyze_sentiment)

json_data['is_fact'] = json_data['subjectivity'] < 0.5  # default threshold? subjectivity < 0.5 = fact
json_data['is_opinion'] = json_data['subjectivity'] >= 0.5

json_data['month'] = json_data['issue_date'].dt.to_period('M')
month_data = json_data.groupby('month').agg(
    avg_polarity=('polarity', 'mean'),
    avg_subjectivity=('subjectivity', 'mean'),
    fact_ratio=('is_fact', 'mean'),  
    opinion_ratio=('is_opinion', 'mean')  
).reset_index()

# 
month_data['month'] = month_data['month'].dt.to_timestamp()
print(month_data.head()) 


sentiment_output = input("Enter the path of the new json file:")
monthly_sentiment_output = input("Enter the path of the new json file for monthly avgs:")
json_data['issue_date'] = json_data['issue_date'].dt.strftime('%Y-%m-%d')
json_data[['issue_date', 'fulltext', 'polarity', 'subjectivity']].to_json(sentiment_output, orient='records', lines=True)
month_data.to_json(monthly_sentiment_output, orient='records', lines=True)
#need to add protection from overwriting with counter, as people will probably be iterating



plt.figure(figsize=(14, 8))

plt.subplot(3, 1, 1)
plt.plot(month_data['month'], month_data['avg_polarity'], color='blue')
plt.title('Monthly Average Polarity')
plt.ylabel('Polarity')
plt.grid(True)

plt.subplot(3, 1, 2)
plt.plot(month_data['month'], month_data['avg_subjectivity'], color='orange')
plt.title('Monthly Average Subjectivity')
plt.ylabel('Subjectivity')
plt.grid(True)

plt.subplot(3, 1, 3)
plt.plot(month_data['month'], month_data['fact_ratio'], label='Fact Ratio', color='green')
plt.plot(month_data['month'], month_data['opinion_ratio'], label='Opinion Ratio', color='red')
plt.title('Fact and Opinion')
plt.ylabel('Ratio')
plt.legend()
plt.grid(True)

plt.tight_layout()
plt.show()