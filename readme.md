# The Marine Record and The Marine Review: DH Exploratory Analysis

These files support the exploration of the Marine Record (1878 – August 1902) and Marine Review (March 1890-October 1935) shipping buiness journals using a variety of digital scholarship tools and techniques. 

For a more accessible presentation of results, visit (librarybeales.github.io/marinemarine)

*** This project has just begun and some areas of work may be incomplete or missing entirely! ***

# Cleaning the json files.

Each process and the relevant visualizations, if any, can be found in its own directory; OCR, text cleaning and processing, topic modeling, entity recognition, geocoding etc.  

Step 1: Run `cleaning\cleaning_userinput.py` to remove line breaks, carriage retursn, multiple spaces, and replace them all with a single space.  This script also converts all text to lowercase.  (Need to separate the `text.lower()` function for entity recognition.)  This script could use some more functions for cleaning various unicode characters, etc.

Step 2:  Use `cleaning\date_format_userinput.py` to reformat the date field to YYYY-MM-DD.

Step 3:  Use `cleaning\merge_by_date_json.py` to create a new json file that has all the `full_text` fields merged for each date.  The original files have separate json records for each page, as they were being used as part of the web interface at (https://images.maritimehistoryofthegreatlakes.ca) where images of the original pages can be viewed.  For our purposes we don't need each page as a separate record, so this script creates one json record for each issue of the Marine Review/Marine Record where all the `full-text` fields are merged, `issue`, `issue_date`, and `issue_id` are maintained and the `page_id` field is removed.  There is another option for just creating a dictionary where the key is the `issue_date` and the value is the mergerd `full_text` fields for this date.  


*** 24 entires of the Marine Review have no day in the date field, it appears to be a special issue about "The Greatest Storm in Lake History" 1914-03-__  Need to edit these dates to make them complete.  Adding day 01. ***  


*** Need to merge `full_text` on `issue` AND `issue_date` to avoid errors in the event that the Marine Record and the Marine Review were published on the same day.  Right now I am working on the two collections separately, but this will come up in the future. ***





## Acknowledgments

The extensive digitization and OCR work that has made this project possible was done by Walter Lewis.  Images of these publications, and advanced search tools for these and many other Great Lakes historical resources can be found at his site.  (https://images.maritimehistoryofthegreatlakes.ca)

## Authors

[LibraryBeales](https://github.com/LibraryBeales)

See also the list of
[contributors](https://github.com/LibraryBeales/marinemarine/contributors)
who participated in this project.

## License

This project is licensed under the [MIT License](https://github.com/LibraryBeales/WORKSHOP TITLE/blob/main/LICENSE)
See the [LICENSE](https://github.com/LibraryBeales/marinemarine/blob/main/LICENSE) file for details.

