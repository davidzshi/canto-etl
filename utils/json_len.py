import json

# find the number of JSON objects in a file

with open('../account_etl/accounts.json') as f:
    data = json.load(f)
    num_objects = len(data)
    print(f'The file contains {num_objects} JSON objects')
