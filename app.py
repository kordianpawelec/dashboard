from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from dotenv import load_dotenv

load_dotenv()
from shared.scripts.importand_days import Holidays
from shared.models.holidays import HolidaysData, UpcomingData
from typing import List
import uvicorn
import psutil


app = FastAPI()
holidays = Holidays()
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/health_check")
def health_check():
    return {"status": "ok"}


@app.get("/metrics")
def metrics():
    return {
        "cpu_percent": psutil.cpu_percent(),
        "ram_percent": psutil.virtual_memory().percent,
        "stroage_percent": psutil.disk_usage("/").percent,
    }


@app.get("/", response_class=HTMLResponse)
def root(request: Request):

    return templates.TemplateResponse(
        "dashboard.html",
        {
            "request": request,
            "endpoints": {
                "/upcoming": "Get upcoming holidays",
                "/add-date": "Add a new holiday",
                "/docs": "Interactive API docs",
                "/redoc": "ReDoc documentation",
                "/metrics": "CPU RAM STORAGE",
                "/health_check": "Health check",
            },
        },
    )


@app.get("/upcoming", response_model=List[UpcomingData])
def upcoming():
    return holidays.check_close_days()


@app.put("/add-date", response_model=HolidaysData)
def update_dates(data: HolidaysData):
    holidays.add_important_days(data)
    return data


if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=8000)
