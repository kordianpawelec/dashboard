from pydantic import BaseModel, RootModel
from typing import List, Dict


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
