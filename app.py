from fastapi import FastAPI, Request, HTTPException, Form
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from dotenv import load_dotenv

load_dotenv()
from shared.scripts.importand_days import Holidays
from shared.schemas import DBController, User, init_db
init_db()
from shared.models.holidays import HolidaysData, UpcomingData
from typing import List
import hashlib
import secrets
import uvicorn, psutil, os


db_controller = DBController()

app = FastAPI()
holidays = Holidays()
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")


def verify_token(token: str):
    if token != os.environ.get('ALLOWED_TOKEN'):
        raise HTTPException(status_code=401, detail="Invalid token")
    return token

@app.post('/register', response_class=HTMLResponse)
async def register(
    request: Request,
    username: str = Form(...),
    email: str = Form(...),
    password: str = Form(...),
    registration_token: str = Form(...)
):
    try:
        verify_token(registration_token)
        
        existing_user = db_controller.get_user_by_username(username)
        if existing_user:
            return """
            <div class="alert alert-error">
                Username already exists!
            </div>
            """
        
        hashed_password = hashlib.sha256(password.encode()).hexdigest()
        user_token = secrets.token_urlsafe(32)
        
        new_user = User(
            username=username,
            email=email,
            hashed_password=hashed_password,
            token=user_token
        )
        
        db_controller.add_user(new_user)
        return f"""
        <div class="alert alert-success">
            <h3>Account Created!</h3>
            <p>Username: {username}</p>
            <p>Your API Token: <code>{user_token}</code></p>
            <p style="color: red;"><strong>Save this token! You'll need it.</strong></p>
        </div>
        """

    except HTTPException as e:
        return f"""
        <div class="alert alert-error">
            {e.detail}
        </div>
        """
    except Exception as e:
        return f"""
        <div class="alert alert-error">
            Error: {str(e)}
        </div>
        """
    
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
