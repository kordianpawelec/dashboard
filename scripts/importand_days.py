import requests
import os
from collections import defaultdict

from datetime import datetime

TOKEN = os.environ.get('DAYS_TOKEN')
YEAR = datetime.now().year

class Holidays:
    def __init__(self):
        pass


    def get_holidays(self, country: str):
        response = requests.get(f'https://calendarific.com/api/v2/holidays?api_key={TOKEN}&country={country}&year={YEAR}')
        response.raise_for_status()
    
        holidays = response.json().get('response').get('holidays')
        
        data = []
        for holiday in holidays:
            data.append({
                'name': holiday.get('name'),
                'date': holiday.get('date').get('iso')})

        return data

    def get_data(self):
        data = defaultdict(list)
        for c in ['pl', 'ie']:
            holidays = self.get_holidays(c)
            
            for holiday in holidays:
                data[holiday['name']].append({'date': holiday['date'], 'country':c})