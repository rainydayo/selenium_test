import requests

# Constants
API_KEY = 'ce142dd123be3f08bb89cb79e2c25654'.strip()  # Ensure no extra spaces
SCOPUS_ID = '85181752598'
BASE_URL = f'https://api.elsevier.com/content/abstract/scopus_id/{SCOPUS_ID}'
HEADERS = {
    'X-ELS-APIKey': API_KEY,
    'Accept': 'application/json'
}

# Fetch Data
response = requests.get(BASE_URL, headers=HEADERS)
if response.status_code == 200:
    data = response.json()
    # Extract the @href link for the Scopus record
    links = data.get('abstracts-retrieval-response', {}).get('coredata', {}).get('link', [])
    scopus_link = next((link['@href'] for link in links if link['@rel'] == 'scopus'), None)
    if scopus_link:
        print(f"Scopus Link: {scopus_link}")
    else:
        print("Scopus link not found.")

    cited_by_count = data.get('abstracts-retrieval-response', {}).get('coredata', {}).get('citedby-count')
    if cited_by_count is not None:
        print(f"Cited By Count: {cited_by_count}")
    else:
        print("Cited By Count: False")
else:
    print(f"Failed to fetch data: {response.status_code} - {response.text}")
