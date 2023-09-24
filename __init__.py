import re
import requests
import json
import logging

import pandas as pd
from bs4 import BeautifulSoup

logging.basicConfig(level=logging.INFO)

PAGE_URL = 'https://www.eventbrite.com/d/germany--berlin/free--events/job-fairs/?lang=de%2Cen'
logging.info(f'Web scrabbing this page url {PAGE_URL}')

current_page = 1
response = requests.get(PAGE_URL)

soup = BeautifulSoup(response.text, 'html.parser')
result_df = pd.DataFrame()

def get_last_page(soup: BeautifulSoup) -> str:
    # set initial pagination
    last_pagination = 1

    try:
        # get footer
        footer = soup.find('footer')
        soup_footer = BeautifulSoup(footer.text, 'html.parser')

        # Use regex to extract the number before 'Next' and after '...'
        result = re.search(r'\.\.\.(\d+)Next', soup_footer.text)

        # Return the extracted number
        if result:
            # Get the number as an integer
            last_pagination = int(result.group(1))
        
        return last_pagination
        
    except Exception as e:
        logging.error(f'An error occurred while retriving last pagination: {e}')
        raise

    finally:
        logging.info(f'Last page of this URL is {last_pagination}')
        

def get_event(page: int = 1) -> BeautifulSoup:
    try:
        global result_df
        url = f'{PAGE_URL}&page={page}]'
        logging.info(f'Retrieving data from page {page}')

        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')

        event_list = soup.find_all('script', type="application/ld+json")
        for i, event_raw in enumerate(event_list):
            event = json.loads(event_raw.text.strip())

            # for debugging json
            # json_string = json.dumps(event, indent=2)
            # print(json_string)

            df = pd.json_normalize(event)
            result_df = result_df._append(df, ignore_index=True)
        
        return soup
    
    except Exception as e:
        logging.error(f'An error occurred while retriving data: {e}')
        raise

def save_to_excel(df, file_path):
    try:
        df.to_excel(file_path, index=False)
    except PermissionError as e:
        logging.error(f'Permission denied while saving file to {file_path}: {e}')
        raise
    except Exception as e:
        logging.error(f'An error occurred while saving file to {file_path}: {e}')
        raise
    finally:
        logging.info(f'Saved file to {file_path}')

first_page_html = get_event()
last_page = get_last_page(first_page_html)

while current_page < last_page:
    current_page += 1
    get_event(current_page)

save_to_excel(result_df, file_path='data/result.xlsx')