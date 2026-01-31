from fastapi import FastAPI
from scripts.importand_days import Holidays
import uvicorn

app = FastAPI()

holidays = Holidays()

@app.get('/')
def main():
    return holidays.get_data()

@app.get('/upcoming')
def upcoming():
    return holidays.check_close_days()


if __name__ == '__main__':
    uvicorn.run('app:app', reload=True)