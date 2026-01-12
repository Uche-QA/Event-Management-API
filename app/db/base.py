from sqlalchemy.orm import DeclarativeBase

class Base(DeclarativeBase):
    pass


from app.models.user import User
from app.models.event import Event
from app.models.rsvp import RSVP