from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship
from app.db.base import Base

class Event(Base):
    __tablename__ = "events"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    owner_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
    owner = relationship("User", back_populates="events")
    description = Column(String)
    location = Column(String)
    date = Column(Date)
    flyer_url = Column(String, nullable=True)

    # Relationship to RSVPs (One-to-Many)
    rsvps = relationship("RSVP", back_populates="event", cascade="all, delete-orphan")