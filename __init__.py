import requests
from bs4 import BeautifulSoup

# response = requests.get('https://oxylabs.io/')
# print(response.text)

# form_data = {'key1': 'value1', 'key2': 'value2'}
# response = requests.post('https://oxylabs.io/', data=form_data)
# print(response.text)

url = 'https://www.eventbrite.com/d/germany--berlin/free--events/job-fairs/?page=1'
response = requests.get(url)

soup = BeautifulSoup(response.text, 'html.parser')
# print(soup.title)

event_sections = soup.find_all('section', class_="discover-horizontal-event-card")

for i, event in enumerate(event_sections):
    
    print('INDEX =============== ', i)

    title = event.find('h2').text.strip()
    link = event.find('a', class_='event-card-link')['href']
    

    p_classes = event.find_all('p')

    date = p_classes[0].text.strip()
    organizer = p_classes[1].text.strip()


    print('title', title)
    print('link', link)
    print('date', date)
    print('organizer', organizer)
