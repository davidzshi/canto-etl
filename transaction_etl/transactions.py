import json
import requests
import time
import os

# Set the maximum number of retries and the initial backoff delay in seconds
MAX_RETRIES = 5
INITIAL_BACKOFF = 1

# Set the path to the accounts and state files
ACCOUNTS_FILE = "../account_etl/accounts.json"
STATE_FILE = "tx_state.json"

# Load the current state from the state file, or start from the beginning if the file doesn't exist
if os.path.exists(STATE_FILE):
    with open(STATE_FILE, "r") as f:
        state = json.load(f)
else:
    state = {"index": 0}

# Open the accounts file and load the account data
with open(ACCOUNTS_FILE, "r") as f:
    accounts = json.load(f)

# Loop through the accounts starting from the last processed index
for i in range(state["index"], len(accounts)):
    item = accounts[i]
    url = f"https://evm.explorer.canto.io/api?module=account&action=txlist&address={item['address']}"
    retries = 0
    backoff = INITIAL_BACKOFF

    # Retry the request with exponential backoff if there is a timeout or connection error
    while retries < MAX_RETRIES:
        try:
            response = requests.get(url)
            if response.ok:
                transactions = response.json()
                break
        except (requests.exceptions.Timeout, requests.exceptions.ConnectionError):
            if retries == MAX_RETRIES - 1:
                raise
            retries += 1
            time.sleep(backoff)
            backoff *= 2

    # Update the state with the current index
    state["index"] = i + 1
    with open(STATE_FILE, "w") as f:
        json.dump(state, f)

    # Skip the item if no transactions were found
    if transactions['status'] == '0':
        continue

    # Write the transactions to the output file with a comma separator
    with open("transactions.json", "a") as f:
        json.dump(transactions['result'], f, indent=2)
        f.write(",\n")
