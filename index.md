# The Marine Record and The Marine Review: DH Exploratory Analysis

These files support the exploration of the Marine Record (1878 – August 1902) and Marine Review (March 1890-October 1935) shipping buiness journals using a variety of digital scholarship tools and techniques. 

For a more accessible presentation of results, visit (librarybeales.github.io/marinemarine)

*** This project has just begun and some areas of work may be incomplete! ***

Each process and the relevant visualizations, if any, can be found in its own directory; OCR, text cleaning and processing, topic modeling, entity recognition, geocoding etc.  

## Acknowledgments

The extensive digitization and OCR work that has made this project possible was done by Walter Lewis.  Images of these publications, and advanced search tools for these and many other Great Lakes historical resources can be found at his site.  (https://images.maritimehistoryofthegreatlakes.ca)

## Cleaning the Text

These steps could reliably be combined into one script.  The processes are separated out here because this project is intended for use in teaching introductory DH workshops so I am breaking it down into more explicit steps and saving each output as a new json file to demonstrate the process and outputs more explicitly.

Step 1: Run `cleaning\cleaning_userinput.py` to remove line breaks, carriage retursn, multiple spaces, and replace them all with a single space.  This script also converts all text to lowercase.  (Need to separate the `text.lower()` function for entity recognition.)  This script could use some more functions for cleaning various unicode characters, etc.

Step 2:  Use `cleaning\date_format_userinput.py` to reformat the date field to YYYY-MM-DD.

Step 3:  Use `cleaning\merge_by_date_json.py` to create a new json file that has all the `full_text` fields merged for each date.  The original files have separate json records for each page, as they were being used as part of the web interface at (https://images.maritimehistoryofthegreatlakes.ca) where images of the original pages can be viewed.  For our purposes we don't need each page as a separate record, so this script creates one json record for each issue of the Marine Review/Marine Record where all the `full-text` fields are merged, `issue`, `issue_date`, and `issue_id` are maintained and the `page_id` field is removed.  There is another option for just creating a dictionary where the key is the `issue_date` and the value is the mergerd `full_text` fields for this date.  

*** Need to merge `full_text` on `issue` AND `issue_date` to avoid errors in the event that the Marine Record and the Marine Review were published on the same day.  Right now I am working on the two collections separately, but this will come up in the future. ***

Cleaning and processing data can reveal interesting anomalies, so error handling should include reporting errors, not just ensuring the script doesn't crash.

In the Marine Review, 24 entries in March 1914 have no day in the date field, and when looking at the josn file, it appears to be a special issue (actually called a supplement) about "The Greatest Storm in Lake History" The 'error' in the date format has shown us a part of the publication that may be of special interest.  As someone who is using the EDA of this collection to learn about Great Lakes Maritime history, the discovery of a special issue in the archive is certainly an exciting one. 

```print(f"Error: The date '{issue_date}' in entry {entry} does not match the expected format '%Y%m%d'.")```

## Word Counts Over Time

The script `words_over_time.py` will prompt the user for a json file that has been cleaned and has the 'issue_date' and 'fulltext' fields in each entry. The script will then ask for terms of interest.  The script will loop though each entry, splitting the text into individual words and create nested dictionaries with counts for each selected word.  The data at that point will look something like this.

```
word_counts_by_date = {
    datetime(1883, 3, 17): {'oil': 3, coal: 1},
    datetime(1883, 3, 31): {'oil': 1, 'steam': 2},
}
```
The nested dictionaries are then flattened into a list of dictionaries, converted to a pandas dataframe, and visualized using matplotlib.

Our initial visualization shows a high level of granularity, but is a bit difficult to read.  It does reveal that there are a couple years of what appears to be missing data.
![coal, iron, oil, steel](https://github.com/LibraryBeales/marinemarine/blob/main/graphics/wordcountsexp5.png?raw=true)

We can try to add a smoothing function that takes a rolling average of a month instead of showing the total for each issue of the Marine Record separately.  Now it is a bit easier to see the trends, but the mising data is a bit hard to identify.  I wonder why the mentions of iron dropped off so suddenly in 1892?
![coal, iron, oil, steel](https://github.com/LibraryBeales/marinemarine/blob/main/graphics/wordcountsexp4.png?raw=true)

Divergence of the terms corn, wheat and grain could be due to a change in nomenclature at that time that groups all grains together.  It may represent just a change in the journal's vocabulary, and not an economic event.
![grain, corn, wheat graph](https://github.com/LibraryBeales/marinemarine/blob/main/graphics/wordcountsexp3.png?raw=true)

TO DO: 
- Add error checking so the script doesn't crash if there is a mising key in a json entry.
- Add a request for user input for smoothing.
- Currently the script ends when you close the visualization.  I'd like it to prompt the user as to whether they'd like to generate additional visualizations.
- Convert the entire visualization piece to plotly so there are interactive elements, such as drop downs for selected words, and the entire thing is more aesthetically pleasing and consistent.
- I'm sure a to do list with only 5 things is incomplete...

Also, I initially had the script count all the words in the corpus before selecting those the user was interested in visualizing.  This created memory problems...  That script is now saved as: `ERROR_words_over_time_input.py` if you are curious aobut how not to do this.  

## Place Names Over Time

Instead of asking for user input, we can show the most mentioned terms from a list of terms in a csv file.  This is very similar to the previous words over time visualization, with input differences.  The csv of place names is currently just the name data.  However, more interesting and complex visualizations and EDA using place names could be available using csv files with census data, industry data, etc., combining that with the Marine Record and Marine Review corpora.

Here we can see place names move together and maintain relateive frequency.  This suggests a few things.  First, that the realtive importance of the Lake Erie ports didn't change much over the course of the Marine Record's publication.  Second, that the publication may include some regular tables of departures/arriveials/etc that constitute the majority of place names used in the publication, creating the consistent movement across terms.  
![placename graph 2](https://github.com/LibraryBeales/marinemarine/blob/main/graphics/placenames2.png?raw=true)
![placename graph 3](https://github.com/LibraryBeales/marinemarine/blob/main/graphics/placenames3.png?raw=true)

If we explore the Marine Review, we discover something very interesting.  A set of place names visualized over the course of the publicaiton shows a marked drop off in the frequency of all place names around 1908-1909.  If we then look at the overall word count, we can see a simlar drop at the same time across all words.  Diving into the raw json data a bit, we can see that publication went from weekly to monthly earlt in 1909, but word count per issue did not quadruple, and in many cases a monthly issue was similar in size to a weekly issue. 

Our EDA visualizations have revealed a change in publishing schedule!

![placename graph 5](https://github.com/LibraryBeales/marinemarine/blob/main/graphics/placenames5.png?raw=true)
![word counts over time](https://github.com/LibraryBeales/marinemarine/blob/main/graphics/wordcountsexp6.png?raw=true)

This is only very obvious in our visualization because we created a new date field that was just month and year, and grouped the word counts by month.  Here's that code:

```
placename_counts_df = pd.DataFrame(placename_counts)
placename_counts_df['issue_date'] = pd.to_datetime(placename_counts_df['issue_date'])
placename_counts_df['year_month'] = placename_counts_df['issue_date'].dt.to_period('M')
placename_counts_df['year_month'] = placename_counts_df['year_month'].astype(str)

monthly_counts = top_places_separated.groupby(['year_month', 'place'])['count'].sum().unstack(fill_value=0)
```

If we simply visualize by publication date, it looks as if the total word counts of the issues is steadily increasing, and the only clue to us that something has changed is the sudden decrease in density of the data points, which is not nearly as obvious at first glance.  

![word counts over time](https://github.com/LibraryBeales/marinemarine/blob/main/graphics/wordcountsexp7.png?raw=true)



## Sentiment Analysis

Show the change in sentiment over time relevant to known and unknown events.  Compare sentiment changes in time of the two publications.


## Topic Modeling

This is an older method is using gensim for LDA, and not the newer options that include transformers, such as BERTopic and Top2Vec. Interactive visualization created by pyLDAvis shows some clustering that may indicate a lack of effective modeling.  The BERTopic model example just uses a lightweight model, not necesarily a model appropriate for this collection.  I'm just beginning to explore this topic modeling option and I have a lot to learn.  Topics from this are more numerous, but not much more diverse.  Much more can be done to improve this as well, I'm sure.  I have a lot to learn about transformers in topic modeling.

The Marine Record and Marine Review are both narrow in scope, so more time tuning and training will likely be required for effective modeling. But there are also obvious problems with cleaning the text, numerals, adding stop words that characterize the domain, etc., etc.   Visualizing the relevance of topics over time will certainly be more interseting in terms of exploring the history of this publication.

Lots to be done here.

Gensim LDA Visualization

(https://rdavidbeales.com/lda_visualization.html)

Gensim LDA Topics
```
Extracted Topics:
Topic 0:
0.009*"new" + 0.008*"cleveland" + 0.008*"marine" + 0.008*"ship" + 0.006*"york" + 0.006*"building" + 0.005*"works" + 0.004*"000" + 0.004*"steam" + 0.004*"chicago" + 0.004*"iron" + 0.004*"steel"
Topic 1:
0.014*"cont" + 0.003*"sch" + 0.002*"cargo" + 0.002*"req" + 0.002*"eee" + 0.002*"coal" + 0.002*"14001" + 0.002*"251" + 0.001*"000" + 0.001*"new" + 0.001*"410" + 0.001*"1919"
Topic 2:
0.001*"ship" + 0.001*"new" + 0.001*"marine" + 0.001*"york" + 0.001*"cleveland" + 0.001*"000" + 0.000*"review" + 0.000*"feet" + 0.000*"water" + 0.000*"steam" + 0.000*"one" + 0.000*"steel"
Topic 3:
0.007*"marine" + 0.007*"feet" + 0.007*"lake" + 0.006*"000" + 0.006*"cleveland" + 0.005*"steam" + 0.005*"new" + 0.005*"vessels" + 0.004*"vessel" + 0.004*"capt" + 0.004*"company" + 0.004*"one"
Topic 4:
0.010*"new" + 0.008*"marine" + 0.006*"york" + 0.005*"ship" + 0.004*"ships" + 0.004*"american" + 0.004*"oil" + 0.004*"000" + 0.004*"feet" + 0.004*"city" + 0.003*"per" + 0.003*"one"
Topic 5:
0.007*"000" + 0.005*"ship" + 0.005*"one" + 0.005*"new" + 0.005*"tons" + 0.004*"two" + 0.004*"vessels" + 0.003*"would" + 0.003*"water" + 0.003*"per" + 0.003*"vessel" + 0.003*"made"
```

BERTopic Visualization

(https://rdavidbeales.com/bertopic_topics.html)

BERTopic Topics (I let the package determine the number of topics.  For LDA, I chose 6.)
```Topics:
Topic 0: 0_co_new_ship_marine
Topic 1: 1_co_cleveland_ee_ship
Topic 2: 2_000_tons_one_lake
Topic 3: 3_000_new_ships_tons
Topic 4: 4_co_new_cleveland_ship
Topic 5: 5_000_co_new_marine
Topic 6: 6_co_new_york_marine
Topic 7: 7_steam_cleveland_lake_feet
Topic 8: 8_000_str_one_co
Topic 9: 9_marine_lake_co_cleveland
Topic 10: 10_ft_000_tons_two
Topic 11: 11_000_co_new_marine
Topic 12: 12_marine_capt_lake_cleveland
Topic 13: 13_new_co_marine_ships
Topic 14: 14_000_tons_ft_one
Topic 15: 15_co_marine_cleveland_new
Topic 16: 16_capt_company_marine_lake
Topic 17: 17_marine_lake_000_vessel
Topic 18: 18_co_feet_new_marine
Topic 19: 19_lake_cleveland_marine_new
Topic 20: 20_lake_marine_steam_st
Topic 21: 21_feet_lake_000_cleveland
Topic 22: 22_co_new_marine_york
Topic 23: 23_ft_one_ee_two
Topic 24: 24_co_cleveland_ee_new
Topic 25: 25_co_new_oil_york
Topic 26: 26_marine_co_st_capt
Topic 27: 27_co_ee_ship_cleveland
Topic 28: 28_marine_lake_cleveland_steam
Topic 29: 29_co_cleveland_new_feet
Topic 30: 30_feet_lake_000_cleveland
Topic 31: 31_000_co_lake_cleveland
Topic 32: 32_co_new_york_city
Topic 33: 33_feet_company_marine_lake
```

Some notes...
https://freedium.cfd/https://medium.com/blend360/topic-modelling-a-comparison-between-lda-nmf-bertopic-and-top2vec-part-i-3c16372d51f0
https://pmc.ncbi.nlm.nih.gov/articles/PMC9120935/
https://freedium.cfd/https://towardsdatascience.com/topic-modeling-with-lsa-plsa-lda-nmf-bertopic-top2vec-a-comparison-5e6ce4b1e4a5

## Entity Recognition

SpaCy

## Authors

[LibraryBeales](https://github.com/LibraryBeales)

See also the list of
[contributors](https://github.com/LibraryBeales/marinemarine/contributors)
who participated in this project.

## License

This project is licensed under the [MIT License](https://github.com/LibraryBeales/WORKSHOP TITLE/blob/main/LICENSE)
See the [LICENSE](https://github.com/LibraryBeales/marinemarine/blob/main/LICENSE) file for details.

