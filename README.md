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
