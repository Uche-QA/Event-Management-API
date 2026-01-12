import os
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

# 1. Database and Base setup
from app.db.session import engine
from app.db.base import Base

# 2. Import ALL models 
from app.models.event import Event
from app.models.rsvp import RSVP
from app.models.user import User  

# 3. Import routers
from app.api.v1.endpoints import event, rsvp, auth
from app.api.v1.endpoints.user import router as user_router

# 4. Create database tables in Postgres
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Event Pro API",
    description="A professional backend for managing events and RSVPs.",
    version="1.0.0"
)

# Ensure upload directory exists
if not os.path.exists("uploads"):
    os.makedirs("uploads")

# Mount static files
app.mount("/static", StaticFiles(directory="uploads"), name="static")

# 5. Include routers
app.include_router(event.router, prefix="/api/v1", tags=["Events"])
app.include_router(rsvp.router, prefix="/api/v1", tags=["RSVPs"])
app.include_router(auth.router, prefix="/api/v1/auth", tags=["auth"])
app.include_router(user_router, prefix="/api/v1/users", tags=["users"])
@app.get("/")
def root():
    return {"message": "Welcome to the Event Pro API! Visit /docs for documentation."}