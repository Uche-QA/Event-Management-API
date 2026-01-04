from pydantic import BaseModel
from datetime import date
from typing import Optional, List
from .rsvp import RSVP  

class EventBase(BaseModel):
    title: str
    description: str
    date: date
    location: str

class EventCreate(EventBase):
    pass

class Event(EventBase):
    id: int
    flyer_url: Optional[str] = None
    

    class Config:
        from_attributes = True