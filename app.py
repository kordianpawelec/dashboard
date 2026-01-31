from fastapi import FastAPI
from scripts.importand_days import Holidays
from models.holidays import HolidaysData, UpcomingData
from typing import List
import uvicorn

app = FastAPI()

holidays = Holidays()

@app.get('/', response_model=List[HolidaysData])
def main():
    return holidays.get_data()

@app.get('/upcoming', response_model=List[UpcomingData])
def upcoming():
    return holidays.check_close_days()


if __name__ == '__main__':
    uvicorn.run('app:app', host='0.0.0.0', port=8000, reload=True)