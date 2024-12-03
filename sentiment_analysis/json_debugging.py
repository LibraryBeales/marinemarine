import pandas as pd

file_path = 'jsons/review_merged_date.json'
data = pd.read_json(file_path)

print(data.head()) 
print(data.columns)  

if data['issue_date'].isnull().all() or data['fulltext'].isnull().all():
    raise ValueError("The 'issue_date' or 'fulltext' columns are empty.")

print(data['issue_date'].isnull().sum())  
print(data['fulltext'].isnull().sum()) 

data['issue_date'] = pd.to_datetime(data['issue_date'], errors='coerce')
print(data['issue_date'].head())