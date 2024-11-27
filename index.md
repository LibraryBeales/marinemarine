# The Marine Record and The Marine Review: DH Exploratory Analysis

These files support the exploration of the Marine Record (1878 – August 1902) and Marine Review (March 1890-October 1935) shipping buiness journals using a variety of digital scholarship tools and techniques. 

For a more accessible presentation of results, visit (librarybeales.github.io/marinemarine)

*** This project has just begun and some areas of work may be incomplete! ***

Each process and the relevant visualizations, if any, can be found in its own directory; OCR, text cleaning and processing, topic modeling, entity recognition, geocoding etc.  

## Acknowledgments

The extensive digitization and OCR work that has made this project possible was done by Walter Lewis.  Images of these publications, and advanced search tools for these and many other Great Lakes historical resources can be found at his site.  (https://images.maritimehistoryofthegreatlakes.ca)

## Cleaning the Text

Cleaning and processing data can reveal interesting anomalies, so error handling should include reporting errors, not just ensuring the script doesn't crash. - Marine Record - 24 entiries of the Marine Review have no day in the date field, it appears to be a special issue about "The Greatest Storm in Lake History" Date format is missing the day.  1914-03-__  Need to edit these dates to make them complete.  Adding day 01.  

```print(f"Error: The date '{issue_date}' in entry {entry} does not match the expected format '%Y%m%d'.")```

These steps could reliably be combined into one script.  The processes are separated out here because this project is intended for use in teaching introductory DH workshops so I am breaking it down into more explicit steps and saving each output as a new json file to demonstrate the process and outputs more explicitly.

Step 1: Run `cleaning\cleaning_userinput.py` to remove line breaks, carriage retursn, multiple spaces, and replace them all with a single space.  This script also converts all text to lowercase.  (Need to separate the `text.lower()` function for entity recognition.)  This script could use some more functions for cleaning various unicode characters, etc.

Step 2:  Use `cleaning\date_format_userinput.py` to reformat the date field to YYYY-MM-DD.

Step 3:  Use `cleaning\merge_by_date_json.py` to create a new json file that has all the `full_text` fields merged for each date.  The original files have separate json records for each page, as they were being used as part of the web interface at (https://images.maritimehistoryofthegreatlakes.ca) where images of the original pages can be viewed.  For our purposes we don't need each page as a separate record, so this script creates one json record for each issue of the Marine Review/Marine Record where all the `full-text` fields are merged, `issue`, `issue_date`, and `issue_id` are maintained and the `page_id` field is removed.  There is another option for just creating a dictionary where the key is the `issue_date` and the value is the mergerd `full_text` fields for this date.  

*** Need to merge `full_text` on `issue` AND `issue_date` to avoid errors in the event that the Marine Record and the Marine Review were published on the same day.  Right now I am working on the two collections separately, but this will come up in the future. ***

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

Instead of asking for user input, we can show the most menioned places from a list of places in a csv file.  This is very similar to the previosu words over time visualization, with input differences.  The csv of place names is currently just the name data.  However, more interesting and complex visualizations and EDA could be available using csv files with census data, industry data, and combiing that with the Marine Record and Marine Review corpora.

![placename graph 1](https://github.com/LibraryBeales/marinemarine/blob/main/graphics/placenames2.png?raw=true)
![placename graph 1](https://github.com/LibraryBeales/marinemarine/blob/main/graphics/placenames3.png?raw=true)


## Sentiment Analysis

Show the change in sentiment over time relevant to known and unknown events.  Compare sentiment changes in time of the two publications.

## Topic Modeling

Compare the two publicaitons?


## Authors

[LibraryBeales](https://github.com/LibraryBeales)

See also the list of
[contributors](https://github.com/LibraryBeales/marinemarine/contributors)
who participated in this project.

## License

This project is licensed under the [MIT License](https://github.com/LibraryBeales/WORKSHOP TITLE/blob/main/LICENSE)
See the [LICENSE](https://github.com/LibraryBeales/marinemarine/blob/main/LICENSE) file for details.

