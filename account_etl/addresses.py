import requests
import json
import time

# Set the base URL for the API
base_url = 'https://evm.explorer.canto.io/api'

# Load the current page number from meta.json
with open('meta.json', 'r') as meta_file:
    meta_data = json.load(meta_file)
    current_page = meta_data.get('current_page', 1)

# Set the parameters for the API request
params = {
    'module': 'account',
    'action': 'listaccounts',
    'offset': 500,
    'page': current_page
}

# Open the output file in write mode
with open('accounts.json', 'w') as f:
    # If we are starting from the first page, write the opening bracket for the JSON array
    if current_page == 1:
        f.write('[')

    # Initialize the retry count and wait time
    retries = 0
    wait_time = 1

    # Loop over all pages of results
    while True:
        # Make the API request
        response = requests.get(base_url, params=params)

        # Check if the response was successful
        if response.status_code == 200:
            # Parse the response JSON
            data = response.json()

            # Check if there are any results on this page
            if not data['result']:
                break

            # Loop over the accounts and write each one to the output file
            for account in data['result']:
                f.write(json.dumps(account) + ',')

            # Increment the page number
            params['page'] += 1

            # If we have reached the end of the current batch of 5000 records, update the current page number in meta.json
            if (params['page'] - 1) % 500 == 0:
                meta_data['current_page'] = params['page']
                with open('meta.json', 'w') as meta_file:
                    json.dump(meta_data, meta_file)

            # Reset the retry count and wait time
            retries = 0
            wait_time = 1
        elif response.status_code == 429:
            # Extract the retry time from the response headers
            retry_after = int(response.headers.get('Retry-After', 0))

            # Calculate the wait time using an exponential backoff strategy
            wait_time = 2 ** retries
            retries += 1

            # Wait for the specified amount of time before trying again
            time.sleep(wait_time)

            print(f'Too many requests, waiting {wait_time} seconds before retrying')

            # Reset the parameters to retry the current page
            params['page'] -= 1
        else:
            # Handle other error codes
            print(f'Request failed with status code {response.status_code}')
            break

    # If we are done, write the closing bracket for the JSON array
    f.write(']')
