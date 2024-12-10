# Web Scraping with Selenium and Pandas

## Purpose of the Project
This project automates the process of web scraping using Selenium and integrates it with pandas to manage and analyze the extracted data. The primary goal is to scrape data from a web page (e.g., titles, FWCI values) and store it in a structured format like a CSV file. Additionally, the project is designed to handle dynamic content, interact with pagination, and update a pre-existing dataset with newly scraped values.

## Features
- **Scrape Dynamic Web Content**: Use Selenium to extract data from elements that are dynamically loaded.
- **Integration with Pandas**: Store and update scraped data in a pandas DataFrame for further processing.
- **Pagination Support**: Automatically navigate through multiple pages of content.
- **Error Handling**: Robust error handling to ensure smooth execution in case of missing elements or navigation errors.

---

## Installation Instructions
Follow the steps below to set up your environment for running this project.

Please see https://selenium-python.readthedocs.io for more details.

### 1. Install Python
Ensure you have Python 3.x installed on your machine. You can download it from [python.org](https://www.python.org/).

### 2. Install Selenium
Install the Selenium library using pip:
```bash
pip install selenium
```

---

## Source Code Details

### 1. noscrape2.py
Fetches data from the Scopus API for a specific year, retrieving document details like titles and api leading to URLs that lead to their respective pages.

### 2. scopus_id.py
Enhances the dataset by using the data retrieved from noscrape2.py to make additional API calls and fetch detailed document information.

### 3. temp.py
Handles web scraping tasks involving pagination. This script interacts with the "Next" button to scrape data across multiple pages.

### 4. main.py
Scrapes FWCI (Field-Weighted Citation Impact) values from URLs retrieved by scopus_id.py and updates the dataset.

### 5. test.py
Fetches data from the Scopus Search API in year 2017 and fetch additional data, just as noscrape2.py.

### 6. 2017.py
Similar to main.py, but focused specifically on scraping and completing the dataset for the year 2017.


