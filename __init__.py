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

# def get_last_page():
#     # get footer
#     footer = soup.find('footer')
#     soup_footer = BeautifulSoup(footer.text, 'html.parser')

#     # Use regex to extract the number before 'Next' and after '...'
#     result = re.search(r'\.\.\.(\d+)Next', soup_footer.text)

#     # Get the number as an integer
#     last_pagination = int(result.group(1))

#     # Return the extracted number
#     return last_pagination

def get_event(page: int = 1):
    url = f'https://www.eventbrite.com/d/germany--berlin/free--events/job-fairs/?page={page}]'
    # events fine
    event_list = soup.find_all('script', type="application/ld+json")

    for i, event_raw in enumerate(event_list):
        event = json.loads(event_raw.text.strip())

        # for debugging json
        # json_string = json.dumps(event, indent=2)
        # print(json_string)

        df = pd.json_normalize(event)

        result_df = result_df._append(df, ignore_index=True)


first_page_html = get_event()

# last_page = get_last_page()

# url = 'https://www.eventbrite.com/d/germany--berlin/free--events/job-fairs/?page=1'
# while current_page <= last_page:
#     print(current_page)

#     current_page += 1


# result_df.to_excel(f'data/result.xlsx', index=False)


# event_sections = soup.find_all('section', class_="discover-horizontal-event-card")

# for i, event in enumerate(event_sections):
    
#     print('INDEX =============== ', i)

#     title = event.find('h2').text.strip()
#     link = event.find('a', class_='event-card-link')['href']
    

#     p_classes = event.find_all('p')

#     date = p_classes[0].text.strip()
#     organizer = p_classes[1].text.strip()

#     print('title', title)
#     print('link', link)
#     print('date', date)
#     print('organizer', organizer)
