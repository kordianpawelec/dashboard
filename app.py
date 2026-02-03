from fastapi import FastAPI
from dotenv import load_dotenv
load_dotenv()
from shared.scripts.importand_days import Holidays
from shared.models.holidays import HolidaysData, UpcomingData
from typing import List
import uvicorn
import psutil



app = FastAPI()
holidays = Holidays()

@app.get('/health_check')
def health_check():
    return {'status': 'ok'}


@app.get('/metrics')
def metrics():
    return {
        'cpu_percent': psutil.cpu_percent(),
        'ram_percent': psutil.virtual_memory().percent,
        'stroage_percent': psutil.disk_usage('/').percent
    }

@app.get('/')
def root():
    return {
        'message': 'Welcome to my API',
        'endpoints': {
            '/upcoming': 'Get upcoming holidays',
            '/add-date': 'Add a new holiday',
            '/docs': 'Interactive API docs',
            '/redoc': 'ReDoc documentation'
        }
    }

@app.get('/upcoming', response_model=List[UpcomingData])
def upcoming():
    return holidays.check_close_days()

@app.put('/add-date', response_model=HolidaysData)
def update_dates(data: HolidaysData):
    holidays.add_important_days(data)
    return data

if __name__ == '__main__':
    uvicorn.run('app:app', host='0.0.0.0', port=8000)