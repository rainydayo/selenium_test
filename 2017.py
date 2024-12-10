import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import requests
import re

# Constants
API_KEY = '468263d1be213487d32be1bf2920d579'.strip()
HEADERS = {'X-ELS-APIKey': API_KEY, 'Accept': 'application/json'}

# Load input files
df = pd.read_csv('Processed_2017.csv')  # File to update
doc = pd.read_csv('Processed_2017.csv')  # Input data for scraping

# Selenium setup
browser = webdriver.Chrome()
url = 'https://id.elsevier.com/as/authorization.oauth2?platSite=SC%2Fscopus&ui_locales=en-US&scope=openid+profile+email+els_auth_info+els_analytics_info+urn%3Acom%3Aelsevier%3Aidp%3Apolicy%3Aproduct%3Aindv_identity&els_policy=idp_policy_indv_identity_plus&response_type=code&redirect_uri=https%3A%2F%2Fwww.scopus.com%2Fauthredirect.uri%3FtxGid%3D507f0e3894a9b413066469a7940b5c5f&state=userLogin%7CtxId%3D69CA86AEF4AA1B134CD5BA66F4E8131D.i-0f41f21a544565082%3A3&authType=SINGLE_SIGN_IN&prompt=login&client_id=SCOPUS'
browser.get(url=url)
html = browser.execute_script("return document.documentElement.outerHTML")
html[:3000]

accept_cookie = WebDriverWait(browser, 5).until(
                    EC.presence_of_element_located((By.ID, 'onetrust-accept-btn-handler'))
                )
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
        return scopus_link
    else:
        return None

def scrape_departments():
    """Scrape department information and return as a list of strings."""
    try:
        # Locate all span elements within the departments list
        department_elements = WebDriverWait(browser, 5).until(
            EC.presence_of_all_elements_located((By.XPATH, "//div[@class='DocumentHeader-module__vg6f0']//ul[@class='DocumentHeader-module__p4B_K']//li[@class='DocumentHeader-module__Ltfqf']/span"))
        )
        
        # Extract the text, split by ',' and take the first item
        departments = [dept.text.split(',')[0].strip() for dept in department_elements if dept.text]
        #print(departments)
        
        return str(departments)  # Return the list of department names
    except TimeoutException:
        return None



def scrape_keywords():
    """Scrape keywords from the page and return as a list of strings."""
    try:
        keyword_elements = WebDriverWait(browser, 5).until(
            EC.presence_of_all_elements_located((By.XPATH, "//div[@id='indexed-keywords']//dd//span/span[@class='Highlight-module__MMPyY']"))
        )
        
        keywords = [el.get_attribute('textContent').strip() for el in keyword_elements if el.get_attribute('textContent')]
        #print(keywords)
        
        return str(keywords)
    except TimeoutException:
        return None


def scrape_subject_area():
    """Scrape subject area from the page."""
    try:
        subject_area_element = WebDriverWait(browser, 5).until(
            EC.presence_of_element_located((By.XPATH, "//a[@id='source-preview-flyout']//em"))
        )
        return subject_area_element.get_attribute('textContent').strip()
    except TimeoutException:
        return None

def scrape_fwci():
    """Scrape FWCI from the page."""
    try:
        fwci_element = WebDriverWait(browser, 5).until(
            EC.presence_of_element_located((By.XPATH, "//span[text()='FWCI']/ancestor::div[@data-testid='count-label-and-value']//span[@data-testid='clickable-count']"))
        )
        fwci_text = fwci_element.text.strip()
        return float(fwci_text) if fwci_text else None
    except TimeoutException:
        return None

def scrape_authors():
    """Scrape author names and return as a list of formatted strings."""
    try:
        # Locate all span elements containing author names
        author_elements = WebDriverWait(browser, 5).until(
            EC.presence_of_all_elements_located((By.XPATH, "//ul[@class='DocumentHeader-module__LpsWx']//li/button/span"))
        )
        
        # Extract and format the author names
        authors = []
        for author in author_elements:
            name = author.get_attribute('textContent').strip()
            if ',' in name:
                lastname, firstname = name.split(',', 1)
                authors.append(f"{firstname.strip()} {lastname.strip()}")
            else:
                authors.append(name)
        print(authors)
        return str(authors)
    except TimeoutException:
        print("Authors not found or timeout occurred.")
        return None

def scrape_cited_count():
    try:
        cited_element = WebDriverWait(browser, 5).until(
            EC.presence_of_element_located((By.XPATH, "//span[text()='Citations in Scopus']/ancestor::div[@data-testid='count-label-and-value']//span[@data-testid='clickable-count']"))
        )
        cited_text = cited_element.text.strip()
        return float(cited_text) if cited_text else None
    except TimeoutException:
        return None

import re

def scrape_ref_count():
    """Scrape the reference count from the page."""
    try:
        # Locate the reference count element
        ref_element = WebDriverWait(browser, 5).until(
            EC.presence_of_element_located((By.XPATH, "//h4[@class='subTitle']"))
        )
        ref_text = ref_element.text.strip() or ref_element.get_attribute('textContent').strip()

        match = re.search(r'\((\d+)\)', ref_text)
        if match:
            return int(match.group(1))
        else:
            return None
    except TimeoutException:
        return None

    
def scrape_publisher():
    try:
        # Locate the <dd> tag containing the publisher
        publisher_element = WebDriverWait(browser, 5).until(
            EC.presence_of_element_located((By.XPATH, "//dl[@data-testid='source-info-entry-publisher']/dd"))
        )
        publisher = publisher_element.get_attribute('textContent').strip()
        print(publisher)
        
        return publisher
    except TimeoutException:
        return None
    

# Main scraping logic
doc_chunk = doc.iloc[1800:]
counter = 1
for index, row in doc_chunk.iterrows():
    print(f"Index: {counter}")
    scopus_id = row['DocumentURL'].split('/')[-1]
    browser.get(fetch_scopus_data(scopus_id))
    
    fwci = scrape_fwci()
    # departments = scrape_departments()
    # keywords = scrape_keywords()
    subject_area = scrape_subject_area()
    # authors = scrape_authors()
    Cited_count = scrape_cited_count()
    Ref_count = scrape_ref_count()
    publisher = scrape_publisher()
    
    df.loc[df['DocumentURL'] == row['DocumentURL'], 'FWCI'] = fwci if fwci else 1  # Default FWCI to 1
    # df.loc[df['DocumentURL'] == row['DocumentURL'], 'departments'] = departments if departments else '[None]'
    # df.loc[df['DocumentURL'] == row['DocumentURL'], 'keywords'] = keywords if keywords else '[None]'
    df.loc[df['DocumentURL'] == row['DocumentURL'], 'subject_areas'] = subject_area if subject_area else 'None'
    # df.loc[df['DocumentURL'] == row['DocumentURL'], 'author_names'] = authors if authors else '[None]'
    df.loc[df['DocumentURL'] == row['DocumentURL'], 'Cited_count'] = Cited_count if Cited_count else 'None'
    df.loc[df['DocumentURL'] == row['DocumentURL'], 'Ref_count'] = Ref_count if Ref_count else 'None'
    df.loc[df['DocumentURL'] == row['DocumentURL'], 'publisher'] = publisher if publisher else 'None'

    counter += 1
    

# Save updated DataFrame
df.to_csv('Processed_2017.csv', index=False)
browser.quit()
