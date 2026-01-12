from pydantic import BaseModel
from enum import Enum
from typing import List, Optional

class RSVPStatus(str, Enum):
    going = "going"
    maybe = "maybe"
    not_going = "not_going"

class RSVPCreate(BaseModel):
    status: RSVPStatus

class RSVPOut(BaseModel):
    id: int
    user_id: int
    event_id: int
    status: RSVPStatus

    class Config:
        from_attributes = True