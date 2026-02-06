import time
import requests
import logging
from dotenv import load_dotenv

load_dotenv()
from typing import List
from shared.scripts.alert import Alerts
from datetime import datetime
from shared.models.holidays import UpcomingData


logging.basicConfig(
    filename="scheduler.log",
    format="%(asctime)s %(levelname)s: %(message)s",
    filemode="w",
)
logger = logging.getLogger(__name__)


class Scheduler:
    def __init__(self):
        self.alert = Alerts()
        self.times_to_remind_at = []
        self.pivot_date = datetime.today()
        self.checked = False
        self.last_send = None
        self.send_again = None
        self.run = True  # Keeping it off for now
        self.sent = False
        print(self.get(), "working")

    def get(self):
        try:
            logging.info("getting data from endpoint")
            response = requests.get("http://dashboard-app:8000/upcoming")
            response.raise_for_status()
            logger.info("data reached", response.json())
            return response.json()

        except Exception as e:
            logger.error(f"Failed to reach the endpoint: {e}")
            return None

    def run_schduler(self):
        while self.run:
            print("running")
            current_day = datetime.today()

            if abs(self.pivot_date - current_day) > 0:
                self.checked = False
                self.pivot_date = current_day
                logger.info(f"New Day {current_day}")

            if not self.checked and current_day == 14:
                self.checked = True
                logger.info(f'daily check at 14:00 {current_day}')
                checked_data = self.get()
                
                if checked_data:
                    self.reminder(checked_data)

            if (
                self.last_send
                and self.send_again
                and abs((self.last_send - datetime.now()).total_seconds()) >= 14400
            ):
                logger.info("Sending second 'today' reminder")
                self.alert.send_email(*self.send_again)
                self.last_send = None
                self.send_again = None

            time.sleep(60 * 20)

    def reminder(self, data: List[UpcomingData]):
        head = ""
        body = ""
        has_today_event = False
        has_upcoming_event = False
        
        for date in data:
            days_until = date.days_until
            name = date.name
            
            if days_until == "Today!":
                has_today_event = True
                head += f"{name} is Today !!!"
                body += f"{name} is happening today!\n"
            elif days_until <= 7 and days_until >= 1:
                today = True
                head += f"{date.get('name')} is in {date.get('days_until')} "
                body += f"{date.get('name')} is Today!"
            logger.info("Sent upcoming events reminder")
        if has_today_event:
            self.send_again = (head, body)
            self.alert.send_email(*self.send_again)
            self.last_send = datetime.now()
            logger.info("Sent upcoming events reminder, will send again in 4 hours")

        elif has_upcoming_event:
            self.alert.send_email(head, body or "Events coming up soon!")
            logger.info("Sent upcoming events reminder")

Scheduler().run_schduler()
