import requests
import os
import logging
import json
from shared.models.holidays import HolidaysData
from collections import defaultdict
from datetime import datetime


logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

TOKEN = os.environ.get('TOKEN')
YEAR = datetime.now().year
BEFORE = 7

class Holidays:
    def __init__(self):
        os.makedirs('data', exist_ok=True)
        self.holidays_path = 'shared/data/holidays.json'
        self.private_days_path = 'shared/data/private_dates.json'



    def get_holidays(self, country: str):
        logging.info(f'requsting API for {country}')
        response = requests.get(f'https://calendarific.com/api/v2/holidays?api_key={TOKEN}&country={country}&year={YEAR}')
        response.raise_for_status()
    
        holidays = response.json().get('response').get('holidays')
        logger.info(f'Fetched {len(holidays)} holidays for {country}')

        data = []
        for holiday in holidays:
            date = holiday.get('date').get('datetime')
            data.append({
                'name': holiday.get('name'),
                'date': f'{date.get("day")}-{date.get("month")}-{date.get("year")}'})
            
        return data

    def get_data(self):
        current_day = datetime.today()
        data = defaultdict(list)
        
        if os.path.isfile(self.private_days_path):
            with open(self.private_days_path, 'r') as f:
                data.update(json.load(f))
                
        if os.path.isfile(self.holidays_path):
            with open(self.holidays_path, 'r') as f:
                cached_data = json.load(f)
                cached_data.update(data)
                harvested_data =  datetime.strptime(cached_data.get('data_harvest_date'), '%Y-%m-%d %H:%M:%S.%f')
                if abs((harvested_data - current_day).days) < 2:
                    logger.info('Using cached data from ' + cached_data.get('data_harvest_date'))
                    return cached_data
                
        logger.info('Fetching fresh data from API...')
        for c in ['pl', 'ie']:
            holidays = self.get_holidays(c)
            
            for holiday in holidays:
                date =  holiday['date']
                name = holiday['name']
                
                if any(date == x['date'] for x in data[name]):
                    continue
                data[name].append({'date': date, 'country':c})
        
        with open(self.holidays_path, 'w') as f:
            time_stamp = {'data_harvest_date': str(current_day)}
            data.update(time_stamp)
            json.dump(data, f)
            
        logger.info('Saved fresh data to cache')
        return data

    def check_close_days(self):
        close_days = []
        data = self.get_data()
        current_day = datetime.today()
        
        for name, dates in data.items():
            if name == 'data_harvest_date':
                continue
        
            for date in dates:
                holiday_date = datetime.strptime(date['date'], '%d-%m-%Y').replace(year=current_day.year)
                days_until = (holiday_date - current_day).days
                if days_until <= BEFORE and days_until >= 0:
                    close_days.append({
                        'name': name,
                        'date': date['date'],
                        'country': date['country'],
                        'days_until': 'Today!' if holiday_date.day == current_day.day else days_until + 1
                    })
                    
        return close_days
    
    def add_important_days(self, data: HolidaysData):
        print(data)
        holiday_data = {data.name: [obj.model_dump() for obj in data.dates]}
        print(holiday_data)
        try:
            if os.path.isfile(self.private_days_path):
                with open(self.private_days_path, 'r') as f:
                    file_data = json.load(f)

            else:
                file_data = {}
            
            with open(self.private_days_path, 'w') as f:
                file_data.update(holiday_data)
                json.dump(file_data, f, indent=2)
            
            logger.info(f'Added {len(holiday_data)} important dates')
            
        except Exception as e:
            logging.error('Error', e)
            raise