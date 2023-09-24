import requests
from bs4 import BeautifulSoup
import json
import pandas as pd
import re

current_page = 1
url = 'https://www.eventbrite.com/d/germany--berlin/free--events/job-fairs'
response = requests.get(url)

soup = BeautifulSoup(response.text, 'html.parser')
result_df = pd.DataFrame()

def get_last_page(soup):
    # get footer
    footer = soup.find('footer')
    soup_footer = BeautifulSoup(footer.text, 'html.parser')

    # Use regex to extract the number before 'Next' and after '...'
    result = re.search(r'\.\.\.(\d+)Next', soup_footer.text)

    # Get the number as an integer
    last_pagination = int(result.group(1))

    # Return the extracted number
    return last_pagination

def get_event(page: int = 1):
    global result_df
    url = f'https://www.eventbrite.com/d/germany--berlin/free--events/job-fairs/?page={page}]'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    # events fine

    event_list = soup.find_all('script', type="application/ld+json")
    for i, event_raw in enumerate(event_list):
        event = json.loads(event_raw.text.strip())

        # for debugging json
        # json_string = json.dumps(event, indent=2)
        # print(json_string)

        df = pd.json_normalize(event)
        result_df = result_df._append(df, ignore_index=True)
    
    return soup


first_page_html = get_event()
last_page = get_last_page(first_page_html)
print(f'last_page, {last_page}')


while current_page < last_page:
    current_page += 1

    # continue with page number 2
    print(current_page)
    get_event(current_page)

result_df.to_excel(f'data/result.xlsx', index=False)