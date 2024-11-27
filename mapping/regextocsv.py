import re
import csv

html_file_path = input("Enter the path to the HTML file: ")

try:
    with open(html_file_path, 'r', encoding='utf-8') as file:
        html = file.read()
except FileNotFoundError:
    print("The file was not found. Please check the path and try again.")
    exit()

matches = re.findall(r'<option value="([^"]+)">', html)

csv_file_path = input("Enter the path to save the CSV file (e.g., output.csv): ")

with open(csv_file_path, 'w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    for match in matches:
        writer.writerow([match])




'''
NO GOOD - This version saves the plane names in one list instead of on separate lines.  

import re
import csv

html_file = input("Enter the file path: ")

with open(html_file, 'r', encoding='utf-8') as file:
        html = file.read()

placenames = re.findall(r'<option value="([^"]+)">', html)

csv_file_path = input("Enter the path to save the CSV file (e.g., output.csv): ")

with open(csv_file_path, 'w', encoding='utf-8') as file:
    file.write(', '.join(placenames))'''




'''with open('greatlakesplaces.csv', 'w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    for placename in placenames:
        writer.writerow([placename])'''



