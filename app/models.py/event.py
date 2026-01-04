from sqlalchemy import Column, Integer, String, Date
from sqlalchemy.orm import relationship
from app.database import Base

class Event(Base):
    __tablename__ = "events"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String)
    location = Column(String)
    date = Column(Date)
    image_url = Column(String, nullable=True)

    # Relationship to RSVPs (One-to-Many)
    rsvps = relationship("RSVP", back_populates="event", cascade="all, delete-orphan")