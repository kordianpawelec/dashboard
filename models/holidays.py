from pydantic import BaseModel
from typing import List



class Dates(BaseModel):
    date: str
    country: str

class Holidays(BaseModel):
    name: str
    dates: List[Dates]

class Upcoming(BaseModel):
    name: str
    date: str
    country: str
    days_until: int