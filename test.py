import requests
import pandas as pd
import time

# Constants
API_KEY = 'ce142dd123be3f08bb89cb79e2c25654'.strip()
BASE_URL = 'https://api.elsevier.com/content/search/scopus'
AFFILIATION_ID = '60028190'  # Chulalongkorn University's affiliation ID
HEADERS = {'X-ELS-APIKey': API_KEY, 'Accept': 'application/json'}
PAGE_SIZE = 25  # Number of results per API request
MAX_ELEMENTS = 2000
OUTPUT_FILE = '2017.csv'

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
        # Extract affiliations and countries
        affiliations = entry.get('affiliation', [])
        #countries = list({aff.get('affiliation-country', '') for aff in affiliations if aff.get('affiliation-country', '')})
        affiliation_names = list({aff.get('affilname', '') for aff in affiliations if aff.get('affilname', '')})
        
        records.append({
            'title': entry.get('dc:title', ''),
            'affiliations': '; '.join(affiliation_names),
        })
    return pd.DataFrame(records)

# Fetch data
year = 2017
all_data = []
for start in range(0, MAX_ELEMENTS, PAGE_SIZE):
    print(f"Fetching records {start} to {start + PAGE_SIZE - 1} for year {year}...")
    results = fetch_documents(start, year)
    if not results:
        break  # Stop fetching if there's an error
    df = parse_results(results)
    if df.empty:
        break  # Stop if no more results
    all_data.append(df)
    time.sleep(1)  # To avoid hitting API rate limits

# Combine all data and save to CSV
if all_data:
    final_df = pd.concat(all_data, ignore_index=True)
    final_df.to_csv(OUTPUT_FILE, index=False)
    print(f"Data for year {year} saved to {OUTPUT_FILE}.")
else:
    print(f"No data found for year {year}.")
