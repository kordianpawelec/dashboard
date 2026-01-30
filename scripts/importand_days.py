import requests
import os
import pprint

TOKEN = os.environ.get('DAYS_TOKEN')


class Holidays:
    def __init__(self):
        self.url = f'https://calendarific.com/api/v2/holidays?api_key={TOKEN}'

    def get_holidays(self):
        response = requests.get(self.url)
        response.raise_for_status()
        
        pprint.pprint(response.json())
        return response.text