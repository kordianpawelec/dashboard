import time
import requests
import logging
from dotenv import load_dotenv
load_dotenv()
from typing import List
from scripts.alert import Alerts
from datetime import datetime
from models.holidays import UpcomingData


logging.basicConfig(filename="scheduler.log",
                    format='%(asctime)s %(levelname)s: %(message)s',
                    filemode='w')
logger = logging.getLogger(__name__)


class Scheduler:
    def __init__(self):
        self.alert = Alerts()
        self.times_to_remind_at = []
        self.pivot_date = datetime.today()
        self.checked = False
        self.last_send = None
        self.send_again = None
        self.run = True

    def get(self):
        try:
            logging.info('getting data from endpoint')
            response =  requests.get('http://localhost:8000/upcoming')
            response.raise_for_status()
            logger.info('data reached', response.json())
            return response.json()
        
        except Exception as e:
            logger.error('Failed to reach the endpoint', e)

    def run_schduler(self):
        while self.run:
            current_day = datetime.today()
            
            if not self.checked and current_day.hour == 14:
                self.checked = not self.checked
                logger.info(f'daily check at {current_day}')
                checked_data = self.get()
                
                if checked_data :
                    self.reminder(checked_data)
            
            if self.last_send and self.send_again and abs((self.last_send - datetime.now()).total_seconds()) >= 14400:
                self.alert.send_email(*self.send_again)
                self.last_send = None
                self.send_again = None
                
            
            if abs((self.pivot_date - current_day).days) > 0:
                self.checked = not self.checked
                self.pivot_date = current_day
            
            time.sleep(60*30)

    def reminder(self, data: List[UpcomingData]):
        head = ''
        body = ''
        today = False
        for date in data:
            if date.days_until != 'Today!':
                head += f'{date.name} is in {date.days_until} '
                if not body:
                    body += f'U still got time!'
            else:
                today = True
                head += f'{date.name} is in {date.days_until} '
                body += f'{date.name} is Today!'
        
        if today:
                self.send_again = (head, body)
                self.alert.send_email(*self.send_again)
                self.last_send = datetime.now()
        else:
            self.alert.send_email(head, body)


Scheduler().run_schduler()