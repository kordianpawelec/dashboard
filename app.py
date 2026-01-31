from fastapi import FastAPI
from scripts.importand_days import Holidays
from models.holidays import Holidays, Dates, Upcoming
from typing import Dict, List
import uvicorn

app = FastAPI()

holidays = Holidays()

@app.get('/', response_class=Dict[str, List[Dates]])
def main():
    return holidays.get_data()

@app.get('/upcoming', response_class=List[Upcoming])
def upcoming():
    return holidays.check_close_days()


if __name__ == '__main__':
    uvicorn.run('app:app', host='0.0.0.0', port=8000, reload=True)