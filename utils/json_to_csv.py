import json
import csv

# convert an unnested JSON file to a CSV file

# Open the input JSON file
with open('transactions.json', 'r') as f:
    data = json.load(f)

# Open the output CSV file in write mode
with open('transactions.csv', 'w', newline='') as f:
    # Create a CSV writer object
    writer = csv.writer(f)

    # Write the header row based on the keys in the first item
    writer.writerow(data[0].keys())

    # Write the data rows
    for item in data:
        writer.writerow(item.values())
