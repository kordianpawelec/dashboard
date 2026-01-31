import requests
import os
from collections import defaultdict

from datetime import datetime

TOKEN = os.environ.get('DAYS_TOKEN')
YEAR = datetime.now().year


class Holidays:
    def __init__(self):
        pass

    def current_day(self):
        current_day = datetime.today().strftime('%d-%m-%Y')

    def get_holidays(self, country: str):
        response = requests.get(f'https://calendarific.com/api/v2/holidays?api_key={TOKEN}&country={country}&year={YEAR}')
        response.raise_for_status()
    
        holidays = response.json().get('response').get('holidays')
        
        holiday.get('date').get('iso')
        
        data = []
        for holiday in holidays:
            date = holiday.get('date').get('datetime')
            data.append({
                'name': holiday.get('name'),
                'date': f'{date.get('day')}-{date.get('month')}-{date.get('year')}'})

        return data

    def get_data(self):
        data = defaultdict(list)
        for c in ['pl', 'ie']:
            holidays = self.get_holidays(c)
            
            for holiday in holidays:
                if holiday['date'] not in data[holiday['name']]:
                    data[holiday['name']].append({'date': holiday['date'], 'country':c})
        
        return data