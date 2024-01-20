import requests
from datetime import datetime, timedelta

now = datetime.now()

past_24_hours = now - timedelta(hours=24)

past_24_hours_str = past_24_hours.strftime('%Y-%m-%dT%H:%M:%S')

response = requests.get('https://api.hh.ru/vacancies', params={
    'text': 'Gamedev',
    'date_from': past_24_hours_str,
    'per_page': 10,
    'order_by': 'publication_time'
})

vacancies = response.json()['items']

print(vacancies)