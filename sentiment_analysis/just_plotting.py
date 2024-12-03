
import pandas as pd
from pattern3.text.en import sentiment  
import json
import matplotlib.pyplot as plt

json_file = input("Enter the file path: ")
with open(json_file, "r") as file:
    json_data = json.load(file)

monthly_data = pd.DataFrame(json_data)

def plot_with_rolling_average(months=3):

    monthly_data['rolling_polarity'] = monthly_data['avg_polarity'].rolling(window=months, center=True).mean()
    monthly_data['rolling_subjectivity'] = monthly_data['avg_subjectivity'].rolling(window=months, center=True).mean()

    plt.figure(figsize=(12, 6))
    
    plt.plot(monthly_data['month'], monthly_data['rolling_polarity'], label='Rolling Polarity', color='blue')
    plt.plot(monthly_data['month'], monthly_data['rolling_subjectivity'], label='Rolling Subjectivity', color='orange')
    
    plt.title(f'{months}-Month Rolling Averages for Sentiment Analysis')
    plt.xlabel('Date')
    plt.ylabel('Sentiment Score')
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()

default_months = 3
months = input(f"Enter the number of months for rolling average (default={default_months}): ")
if months.isdigit():
    months = int(months)
else:
    months = default_months

plot_with_rolling_average(months)