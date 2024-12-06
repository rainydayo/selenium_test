import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, StaleElementReferenceException

df = pd.read_csv('Project_DSDE.csv')
df['FWCI'] = 1
# mock_data = {
#     'title': 'Prediction of the Mechanical Behaviour of HDPE Pipes Using the Artificial Neural Network Technique',
#     'year': '2023',  # Placeholder year
#     'author_names': 'John Doe, Jane Smith',  # Placeholder authors
#     'countries': 'USA, UK',  # Placeholder countries
#     'departments': 'Department A, Department B',  # Placeholder departments
#     'affiliations': 'Affiliation X, Affiliation Y',  # Placeholder affiliations
#     'keywords': 'Keyword1, Keyword2',  # Placeholder keywords
#     'subject_areas': 'Mathematics, Computer Science',  # Placeholder subject areas
#     'FWCI': 1.0  # Placeholder FWCI
# }
# df = pd.concat([df, pd.DataFrame([mock_data])], ignore_index=True)
# print(df.shape)
# print(df.info())
# print(df[df['title'] == 'Note on Fourier Transform of Hidden Variable Fractal Interpolation'])

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

url = 'https://www.scopus.com/pages/organization/60028190'
browser.get(url=url)

learn_more_button = WebDriverWait(browser, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//span[text()='Documents']/ancestor::div[@data-testid='count-label-and-value']//span[@data-testid='clickable-count']"))
    )
learn_more_button.click()

input_from = WebDriverWait(browser, 10).until(
    EC.element_to_be_clickable((By.XPATH, "//input[@placeholder='from']"))
)
input_from.clear()
input_from.send_keys("2018")

input_to = WebDriverWait(browser, 10).until(
    EC.element_to_be_clickable((By.XPATH, "//input[@placeholder='to']"))
)

input_to.send_keys("2023")
browser.execute_script("arguments[0].value = arguments[1];", input_to, "2023")

apply_button = WebDriverWait(browser, 10).until(
    EC.element_to_be_clickable((By.CSS_SELECTOR, "button[data-testid='apply-facet-range']"))
)
apply_button.click()

link = WebDriverWait(browser, 10).until(
    EC.element_to_be_clickable((By.CSS_SELECTOR, "a.Button-module__f8gtt.Button-module__rphhF.Button-module__VBKvn.Button-module__ZS4lL.Button-module__hK_LA.Button-module__qDdAl.Button-module__rTQlw"))
)
link.click()

counter = 1
reload_attempted = False  # Track if the page has been reloaded

while True:
    try:
        # Locate and process the title element
        try:
            title_element = WebDriverWait(browser, 10).until(
                EC.presence_of_element_located((By.XPATH, "//h2[@data-testid='publication-titles']/span[@class='Highlight-module__MMPyY']"))
            )
            title_text = title_element.text.strip()
            print(f"Title {counter + 1}: {title_text}")
        except StaleElementReferenceException:
            print("Stale element reference detected. Re-locating title element...")
            title_element = WebDriverWait(browser, 10).until(
                EC.presence_of_element_located((By.XPATH, "//h2[@data-testid='publication-titles']/span[@class='Highlight-module__MMPyY']"))
            )
            title_text = title_element.text.strip()
            print(f"Title {counter + 1}: {title_text}")

        # Check if the title is in the DataFrame (replace df with your DataFrame)
        if title_text in df['title'].values:
            print("This title is in the dataframe.")

            # Attempt to locate and process the FWCI value
            try:
                fwci_element = WebDriverWait(browser, 5).until(
                    EC.presence_of_element_located((By.XPATH, "//span[text()='FWCI']/ancestor::div[@data-testid='count-label-and-value']//span[@data-testid='clickable-count']"))
                )
                fwci_value = float(fwci_element.text.strip())
                print(f"FWCI: {fwci_value}")
                # Update the FWCI value in the DataFrame
                df.loc[df['title'] == title_text, 'FWCI'] = fwci_value
            except TimeoutException:
                print("FWCI not found for this title.")
        else:
            print("Title not found in the dataframe. Skipping to next title.")

        # Find and click the "Next" button to navigate to the next page
        try:
            next_button = WebDriverWait(browser, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//li[@class='nextLink']/a"))
            )
            next_button.click()
            print("Navigated to the next page.")
            reload_attempted = False  # Reset reload flag after successful navigation
            counter +=1
        except TimeoutException:
            print("No 'Next' button found.")
            if not reload_attempted:
                print("Reloading the page and retrying...")
                browser.refresh()
                reload_attempted = True  # Mark that the page has been reloaded
            else:
                print("No 'Next' button found after refresh. Exiting pagination.")
                break

    except Exception as e:
        print(f"An error occurred: {e}")
        break

# print(df[df['title'] == 'Prediction of the Mechanical Behaviour of HDPE Pipes Using the Artificial Neural Network Technique'])
df.to_csv('Processed_FWCI_DSDE.csv', index=False)
