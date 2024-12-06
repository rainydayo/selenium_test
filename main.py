import math
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, StaleElementReferenceException
import requests

# Constants
API_KEY = 'ce142dd123be3f08bb89cb79e2c25654'.strip()  # Replace with your API key
HEADERS = {
    'X-ELS-APIKey': API_KEY,
    'Accept': 'application/json'
}
# Edit these lines to run each individual year
df = pd.read_csv('Project_DSDE_2018.csv')
doc = pd.read_csv('2018.csv')
df['FWCI'] = 1

browser = webdriver.Chrome()
url = 'https://id.elsevier.com/as/authorization.oauth2?platSite=SC%2Fscopus&ui_locales=en-US&scope=openid+profile+email+els_auth_info+els_analytics_info+urn%3Acom%3Aelsevier%3Aidp%3Apolicy%3Aproduct%3Aindv_identity&els_policy=idp_policy_indv_identity_plus&response_type=code&redirect_uri=https%3A%2F%2Fwww.scopus.com%2Fauthredirect.uri%3FtxGid%3D507f0e3894a9b413066469a7940b5c5f&state=userLogin%7CtxId%3D69CA86AEF4AA1B134CD5BA66F4E8131D.i-0f41f21a544565082%3A3&authType=SINGLE_SIGN_IN&prompt=login&client_id=SCOPUS'
browser.get(url=url)
html = browser.execute_script("return document.documentElement.outerHTML")
html[:3000]

accept_cookie = browser.find_element(By.ID, 'onetrust-accept-btn-handler')
accept_cookie.click()

login_element = browser.find_element(By.NAME, 'pf.username')
login_element.clear()
login_element.send_keys('6633122121@student.chula.ac.th')
browser.find_element(By.ID, 'bdd-elsPrimaryBtn').click()

password = browser.find_element(By.ID, 'bdd-password')
password.clear()
password.send_keys('U*P8w:DZ-Aa7p5^')

browser.find_element(By.ID, 'bdd-elsPrimaryBtn').click()

def fetch_scopus_data(scopus_id):
    """Fetch Scopus Link and Cited By Count for a given Scopus ID."""
    base_url = f'https://api.elsevier.com/content/abstract/scopus_id/{scopus_id}'
    response = requests.get(base_url, headers=HEADERS)
    if response.status_code == 200:
        result = response.json()
        links = result.get('abstracts-retrieval-response', {}).get('coredata', {}).get('link', [])
        scopus_link = next((link['@href'] for link in links if link['@rel'] == 'scopus'), None)
        cited_by_count = result.get('abstracts-retrieval-response', {}).get('coredata', {}).get('citedby-count', 'False')
        return scopus_link, cited_by_count
    else:
        return None, None

counter = 1
for index, row in doc.iterrows():
    print(f"Index: {counter}")
    if row['Title'] in df['title'].values:
        scopus_id = row['DocumentURL'].split('/')[-1]
        scopus_link, cited_by_count = fetch_scopus_data(scopus_id)
        if cited_by_count is not None:
            browser.get(url=scopus_link)
            try:
                fwci_element = WebDriverWait(browser, 5).until(
                    EC.presence_of_element_located((By.XPATH, "//span[text()='FWCI']/ancestor::div[@data-testid='count-label-and-value']//span[@data-testid='clickable-count']"))
                )
                fwci_value = float(fwci_element.text.strip())
                print(f"FWCI: {fwci_value}")
                # Update the FWCI value in the DataFrame
                df.loc[df['title'] == row['Title'], 'FWCI'] = fwci_value
            except TimeoutException:
                print("FWCI not found for this title.")
    counter += 1

df.to_csv('Processed_2018.csv', index=False)

