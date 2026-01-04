from pydantic import BaseModel

class RSVPBase(BaseModel):
    name: str
    email: str

class RSVPCreate(RSVPBase):
    pass


class RSVP(RSVPBase):
    id: int
    event_id: int

    class Config:
        from_attributes = True