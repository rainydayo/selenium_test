import requests
import pandas as pd
import os
import time

# Constants
API_KEY = 'ce142dd123be3f08bb89cb79e2c25654'.strip()  # Replace with your API key
BASE_URL = 'https://api.elsevier.com/content/search/scopus'
AFFILIATION_ID = '60028190'  # Chulalongkorn University's affiliation ID
HEADERS = {'X-ELS-APIKey': API_KEY, 'Accept': 'application/json'}
PAGE_SIZE = 25  # Maximum results per request (adjust as needed, up to 200)
OUTPUT_FILE = '2023.csv'  # Existing file to append data

def fetch_documents(start, year):
    """Fetch documents from Scopus API for a specific year."""
    params = {
        'query': f'af-id({AFFILIATION_ID}) AND PUBYEAR = {year}',
        'start': start,
        'count': PAGE_SIZE
    }
    response = requests.get(BASE_URL, headers=HEADERS, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error: {response.status_code}, {response.text}")
        return None

def parse_results(data):
    """Parse JSON results into a pandas DataFrame."""
    entries = data.get('search-results', {}).get('entry', [])
    records = []
    for entry in entries:
        records.append({
            'Title': entry.get('dc:title', ''),
            'DocumentURL': entry.get('prism:url', '')
        })
    return pd.DataFrame(records)

def append_to_csv(df, file_path):
    """Append DataFrame to CSV file."""
    if not os.path.exists(file_path):
        # If the file doesn't exist, create it with a header
        df.to_csv(file_path, index=False)
    else:
        # Append to existing file without writing the header again
        df.to_csv(file_path, mode='a', index=False, header=False)

# Fetch data for a specific year
year = 2023  # Change this for each year manually
all_data = []
for start in range(0, 5000, PAGE_SIZE):  # Up to 5000 results per year
    print(f"Fetching records {start} to {start + PAGE_SIZE - 1} for year {year}...")
    results = fetch_documents(start, year)
    if not results:
        break  # Stop fetching if there's an error
    df = parse_results(results)
    if df.empty:
        break  # Stop if no more results
    all_data.append(df)
    time.sleep(1)  # Avoid hitting rate limits

# Combine data and append to CSV
if all_data:
    final_df = pd.concat(all_data, ignore_index=True)
    append_to_csv(final_df, OUTPUT_FILE)
    print(f"Data for year {year} appended to {OUTPUT_FILE}.")
else:
    print(f"No data found for year {year}.")
