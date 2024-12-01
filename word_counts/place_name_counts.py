#This is a big mess.  I'm just editing it in response to a series of datatype and format errors and really needs some serious cleaning.


import json
import pandas as pd
import matplotlib.pyplot as plt
import re

json_file = input("Enter the file path: ")

# Load JSON data
with open(json_file, "r") as file:
    json_data = json.load(file)

json_data_df = pd.DataFrame(json_data)

#place_names = pd.read_csv("mapping/placenames.csv", header=None, names=["place_name"])  #no header in our csv, so I needed to assign one here.  Could remake the csv with a header.
#places = place_names['place_name'].tolist()

#Load the CSV
place_names = pd.read_csv("mapping/portstest.csv", header=None, names=["place_name"])
place_names['place_name'] = place_names['place_name'].str.strip()  # Remove extra spaces
places = place_names['place_name'].tolist()

print("Place Names:", places)

placename_counts = []

for _, row in json_data_df.iterrows():
    issue_date = row['issue_date']
    fulltext = row['fulltext'].lower()  # Case insensitive matching
    counts = {place: len(re.findall(rf'\b{place.lower()}\b', fulltext)) for place in places}
    counts['issue_date'] = issue_date
    placename_counts.append(counts)

placename_counts_df = pd.DataFrame(placename_counts)
placename_counts_df['issue_date'] = pd.to_datetime(placename_counts_df['issue_date'])
placename_counts_df['year_month'] = placename_counts_df['issue_date'].dt.to_period('M')
placename_counts_df['year_month'] = placename_counts_df['year_month'].astype(str)

print("Columns in placename_counts_df:", placename_counts_df.columns)#debugging
print("First few rows of placename_counts_df:", placename_counts_df.head())#debugging

melted_placenames = placename_counts_df.melt(id_vars="year_month", var_name="place", value_name="count")

print("Columns in melted_placenames:", melted_placenames.columns)#debugging
print("First few rows of melted_placenames:", melted_placenames.head())#debugging

melted_placenames['count'] = pd.to_numeric(melted_placenames['count'], errors='coerce')

# Use nlargest() to select the number of placenames to graph
top_places = melted_placenames.groupby("place")['count'].sum().nlargest(5).index
top_places_separated = melted_placenames[melted_placenames['place'].isin(top_places)]

print("Columns - top_places_separated:", top_places_separated.columns)

if 'year_month' not in top_places_separated.columns:
    top_places_separated['year_month'] = pd.to_datetime(top_places_separated['year_month'], errors='coerce')

monthly_counts = top_places_separated.groupby(['year_month', 'place'])['count'].sum().unstack(fill_value=0)

print("Rows of monthly_counts:", monthly_counts.head()) #debugging

#window is rolling average of taht many months.
monthly_counts_smoothed = monthly_counts.rolling(window=3, axis=0).mean()

monthly_counts.plot(kind="line", stacked=True, figsize=(14, 8))
plt.title("Frequency of Ports Over Time in the Marine Review")
plt.xlabel("Year-Month")
plt.ylabel("Frequency")
plt.legend(title="Locations")
plt.grid(True)
plt.tight_layout()
plt.show()

'''

import json
import pandas as pd
import matplotlib.pyplot as plt
import re

json_file = input("Enter the file path: ")

# Load JSON data
with open(json_file, "r") as file:
    json_data = json.load(file)

json_data_df = pd.DataFrame(json_data)

#place_names = pd.read_csv("mapping/placenames.csv", header=None, names=["place_name"])  #no header in our csv, so I needed to assign one here.  Could remake the csv with a header.
#places = place_names['place_name'].tolist()

#Load the CSV
place_names = pd.read_csv("mapping//testplacenames.csv", header=None, names=["place_name"])
place_names['place_name'] = place_names['place_name'].str.strip()  # Remove extra spaces
places = place_names['place_name'].tolist()

print("Place Names:", places)

# Initialize a DataFrame to store counts
placename_counts = []

# Count each place name on each date
for _, row in json_data_df.iterrows():
    issue_date = row['issue_date']
    fulltext = row['fulltext'].lower()  # Case insensitive matching
    counts = {place: len(re.findall(rf'\b{place.lower()}\b', fulltext)) for place in places}
    counts['issue_date'] = issue_date
    print(f"Issue Date: {issue_date}, Counts: {counts}")  # Debugging output
    placename_counts.append(counts)

placename_counts_df = pd.DataFrame(placename_counts)
placename_counts_df['issue_date'] = pd.to_datetime(placename_counts_df['issue_date'])
placename_counts_df['year_month'] = placename_counts_df['issue_date'].dt.to_period('M')
placename_counts_df['year_month'] = placename_counts_df['year_month'].astype(str)

print(placename_counts_df.columns)
print(placename_counts_df.head())

melted_placenames = placename_counts_df.melt(id_vars="issue_date", var_name="place", value_name="count")
melted_placenames['count'] = pd.to_numeric(melted_placenames['count'], errors='coerce')

# Use nlargest() to select the number of placenames to graph
top_places = melted_placenames.groupby("place")['count'].sum().nlargest(8).index
top_places_separated = melted_placenames[melted_placenames['place'].isin(top_places)]

monthly_counts = top_places_separated.groupby(['year_month', 'place'])['count'].sum().unstack(fill_value=0)

print(monthly_counts.head())
# Plot
#don't need to pivot, using unstack instead, apparently this is better for groupby?
#pivot_top_placenames = top_places_separated.pivot(index="issue_date", columns="place", values="count").fillna(0)
monthly_counts.plot(kind="line", stacked=True, figsize=(14, 8))
plt.title("Frequency of Top 10 Place Names Over Time")
plt.xlabel("Date")
plt.ylabel("Frequency")
plt.legend(title="Place Names")
plt.tight_layout()
plt.show()
'''