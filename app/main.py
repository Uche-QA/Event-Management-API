import os
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from app.database import engine, Base


from app.models.event import Event
from app.models.rsvp import RSVP


from app.routers import events, rsvps


from database import engine, Base
from app.models import event

from routers import events, rsvps

Base.metadata.create_all(bind=engine)



app = FastAPI(
    title="Event Pro API",
    description="A professional backend for managing events and RSVPs.",
    version="1.0.0"
)

if not os.path.exists("uploads"):
    os.makedirs("uploads")


app.mount("/static", StaticFiles(directory="uploads"), name="static")


app.include_router(events.router)
app.include_router(rsvps.router)

@app.get("/")
def root():
    return {"message": "Welcome to the Event Pro API! Visit /docs for documentation."}