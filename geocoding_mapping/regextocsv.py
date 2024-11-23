import re

html_file = input("Enter the file path: ")

with open(html_file, 'r', encoding='utf-8') as file:
        html = file.read()

placenames = re.findall(r'<option value="([^"]+)">', html)

with open('places.csv', 'w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    for placename in placenames:
        writer.writerow([placenames])
