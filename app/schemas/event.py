from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List

class EventBase(BaseModel):
    title: str
    description: Optional[str] = None
    location: Optional[str] = None
    start_time: datetime
    capacity: int = 100
    is_public: bool = True

class EventCreate(EventBase):
    pass

class EventUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    location: Optional[str] = None
    start_time: Optional[datetime] = None
    capacity: Optional[int] = None
    is_public: Optional[bool] = None

class EventOut(EventBase):
    id: int
    owner_id: int
    flyer_url: Optional[str] = None

    class Config:
        from_attributes = True