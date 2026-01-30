import requests
import os
import json
from datetime import datetime

TOKEN = os.environ.get('DAYS_TOKEN')
COUNTRY = 'ie'
YEAR = datetime.now().year

class Holidays:
    def __init__(self):
        self.url = f'https://calendarific.com/api/v2/holidays?api_key={TOKEN}&country={COUNTRY}&year={YEAR}'

    def get_holidays(self):
        response = requests.get(self.url)
        response.raise_for_status()
        
        holidays = json.loads(response.json()).get('response').get('holidays')
        
        return holidays