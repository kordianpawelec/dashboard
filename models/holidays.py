from pydantic import BaseModel
from typing import List



class DatesData(BaseModel):
    date: str
    country: str

class HolidaysData(BaseModel):
    name: str
    dates: List[DatesData]

class UpcomingData(BaseModel):
    name: str
    date: str
    country: str
    days_until: int