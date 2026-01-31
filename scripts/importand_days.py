import requests
import os
import json
from collections import defaultdict

from datetime import datetime

TOKEN = os.environ.get('DAYS_TOKEN')
YEAR = datetime.now().year
BEFORE = 7

class Holidays:
    def __init__(self):
        pass



    def get_holidays(self, country: str):
        print('requesting api...')
        response = requests.get(f'https://calendarific.com/api/v2/holidays?api_key={TOKEN}&country={country}&year={YEAR}')
        response.raise_for_status()
    
        holidays = response.json().get('response').get('holidays')
        
        data = []
        for holiday in holidays:
            date = holiday.get('date').get('datetime')
            data.append({
                'name': holiday.get('name'),
                'date': f'{date.get('day')}-{date.get('month')}-{date.get('year')}'})
            
        return data

    def get_data(self):
        current_day = datetime.today()
        data = defaultdict(list)
        
        if os.path.isfile('data/holidays.json'):
            with open('data/holidays.json', 'r') as f:
                cached_data = json.load(f)
                harvested_data =  datetime.strptime(cached_data.get('data_harvest_date'), '%Y-%m-%d %H:%M:%S.%f')
                if abs((harvested_data - current_day).days) < 2:
                    return cached_data
                

        for c in ['pl', 'ie']:
            holidays = self.get_holidays(c)
            os.makedirs('data', exist_ok=True)
            
            for holiday in holidays:
                date =  holiday['date']
                name = holiday['name']
                
                if any(date == x['date'] for x in data[name]):
                    continue
                data[name].append({'date': date, 'country':c})
        
        with open('data/holidays.json', 'w') as f:
            time_stamp = {'data_harvest_date': str(current_day)}
            data.update(time_stamp)
            json.dump(data, f)
        return data

    def check_close_days(self):
        close_days = []
        data = self.get_data()
        current_day = datetime.today()
        
        for name, dates in data.items():
            if name == 'data_harvest_date':
                continue
        
            for date in dates:
                holiday_date = datetime.strptime(date['date'], '%d-%m-%Y')
                days_until = abs(holiday_date - current_day).days
                if days_until <= BEFORE:
                    close_days.append({
                        'name': name,
                        'date': date['date'],
                        'country': date['country'],
                        'days_until': days_until
                    })
                    
        return close_days