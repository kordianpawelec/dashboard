from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from dotenv import load_dotenv
load_dotenv()
from scripts.importand_days import Holidays
from models.holidays import HolidaysData, UpcomingData
from typing import List
import uvicorn


app = FastAPI()
holidays = Holidays()

@app.get('/health_check')
def health_check():
    return {'status': 'ok'}




@app.get('/', response_class=HTMLResponse)
def get_chart():
    return '''
    <html>
        <body>
            <img src="https://scontent-dub4-1.xx.fbcdn.net/v/t39.30808-6/342919486_593406119408537_3655248339324129439_n.jpg?_nc_cat=107&ccb=1-7&_nc_sid=6ee11a&_nc_ohc=FfgXIMBURcQQ7kNvwH1_sUy&_nc_oc=AdlJD7uJFkHfiTIYkxVfNT1ub7D_s231ZZlGZBJGN7pApGOd8lg9Ssx0YSzNwqYBnWs&_nc_zt=23&_nc_ht=scontent-dub4-1.xx&_nc_gid=dPF-kC1IjTU66zsn8C8U3w&oh=00_AfvPFfN3aPHFxV4ywrCYtfDhNwrO6VhnkyBAD5tl_B9B3g&oe=6987068C" />
        </body>
    </html>
    '''
@app.get('/upcoming', response_model=List[UpcomingData])
def upcoming():
    return holidays.check_close_days()

@app.put('/add-date', response_model=HolidaysData)
def update_dates(data: HolidaysData):
    holidays.add_important_days(data)
    return data

if __name__ == '__main__':
    uvicorn.run('app:app', host='0.0.0.0', port=8000)