import re
import csv

html_file = input("Enter the file path: ")

with open(html_file, 'r', encoding='utf-8') as file:
        html = file.read()

placenames = re.findall(r'<option value="([^"]+)">', html)

csv_file_path = input("Enter the path to save the CSV file (e.g., output.csv): ")

with open(csv_file_path, 'w', encoding='utf-8') as file:
    file.write(', '.join(placenames))




'''with open('greatlakesplaces.csv', 'w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    for placename in placenames:
        writer.writerow([placename])'''


