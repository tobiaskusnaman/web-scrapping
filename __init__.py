import requests
from bs4 import BeautifulSoup
import json
import pandas as pd

url = 'https://www.eventbrite.com/d/germany--berlin/free--events/job-fairs/?page=1'
response = requests.get(url)

soup = BeautifulSoup(response.text, 'html.parser')

event_list = soup.find_all('script', type="application/ld+json")

result_df = pd.DataFrame()

for i, event_raw in enumerate(event_list):
    event = json.loads(event_raw.text.strip())

    # for debugging json
    # json_string = json.dumps(event, indent=2)
    # print(json_string)

    df = pd.json_normalize(event)

    result_df = result_df._append(df, ignore_index=True)
    

result_df.to_excel(f'data/result.xlsx', index=False)

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
