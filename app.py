from fastapi import FastAPI, Request, UploadFile, Form, File, Depends
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, FileResponse
from dotenv import load_dotenv
from sqlalchemy.orm import Session
load_dotenv()
from shared.scripts.importand_days import Holidays
from shared.schemas import init_db, get_db
init_db()
from shared.models.holidays import HolidaysData, UpcomingData
from typing import List
import uvicorn, psutil
from shared.api_logic import APILogic


app = FastAPI()
crud_service = APILogic()
holidays = Holidays()
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")


@app.post('/register')
async def register(
    db: Session = Depends(get_db),
    username: str = Form(...),
    email: str = Form(...),
    password: str = Form(...),
    # registration_token: str = Form(...)
):
    return crud_service.register_user(username=username, email=email, password=password, session=db)


@app.get("/download/{user_id}/{file_id}")
async def download_file(user_id: int, file_id: int, db: Session = Depends(get_db)):
    return await crud_service.download_file(
        user_id=user_id,
        file_id=file_id,
        session=db
    )

@app.get("/list_files/{user_id}")
async def list_files(user_id: int, db: Session = Depends(get_db)):
    return await crud_service.list_files(user_id=user_id, session=db)

@app.post('/upload/{user_id}')
async def upload_file(
    user_id: str,
    db: Session = Depends(get_db),
    file: UploadFile = File(...)
):
    return crud_service.upload_file(
        session=db,
        user_id=user_id,
        file=file
    )


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
        {"request": request, "endpoints": {
            "/docs": "API docs",
            "/register": "Register",
            "/login": "Login",
            "/upload/{user_id}": "Upload file",
            "/files/{user_id}": "List files",
            "/download/{user_id}/{file_id}": "Download",
        }},
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
