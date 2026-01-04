import os
import uuid
import shutil
from typing import List, Optional
from datetime import date
from fastapi import APIRouter, Depends, HTTPException, status, File, UploadFile, Form
from sqlalchemy.orm import Session

# Database and Core logic
from app.database import get_db

# Direct file imports to avoid __init__.py issues
from app.models.event import Event
from app.models.rsvp import RSVP
from app.schemas.event import EventCreate, Event as EventSchema
from app.schemas.rsvp import RSVPCreate, RSVP as RSVPSchema

router = APIRouter(
    prefix="/events",
    tags=["Events"]
)

IMAGEDIR = "uploads/"

# 1. Create the Router
router = APIRouter(
    prefix="/events",
    tags=["Events"]
)

IMAGEDIR = "uploads/"

# 2. POST (Create Event + Upload)
@router.post("/", response_model=schemas.Event, status_code=status.HTTP_201_CREATED)
def create_event(
    title: str = Form(...),
    description: str = Form(...),
    date: date = Form(...),
    location: str = Form(...),
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    # Generate unique filename
    file.filename = f"{uuid.uuid4()}.jpg"
    contents = await file.read()
    
    # Save to disk
    with open(f"{IMAGEDIR}{file.filename}", "wb") as f:
        f.write(contents)
    
    # Save to DB
    path = f"{IMAGEDIR}{file.filename}"
    new_event = models.Event(
        title=title, 
        description=description, 
        date=date, 
        location=location, 
        flyer_url=path
    )
    
    db.add(new_event)
    db.commit()
    db.refresh(new_event)
    return new_event

# 3. GET All (With Search & Pagination)
@router.get("/", response_model=List[schemas.Event])
def get_events(
    skip: int = 0, 
    limit: int = 10, 
    title: Optional[str] = None, 
    db: Session = Depends(get_db)
):
    query = db.query(models.Event)
    if title:
        query = query.filter(models.Event.title.ilike(f"%{title}%"))
    return query.offset(skip).limit(limit).all()

# 4. GET Single Event
@router.get("/{id}", response_model=schemas.Event)
def get_event(id: int, db: Session = Depends(get_db)):
    event = db.query(models.Event).filter(models.Event.id == id).first()
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")
    return event

# 5. DELETE (Cleanup DB + File)
@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_event(id: int, db: Session = Depends(get_db)):
    event = db.query(models.Event).filter(models.Event.id == id).first()
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")
    
    # Delete the physical file
    if os.path.exists(event.flyer_url):
        os.remove(event.flyer_url)
        
    db.delete(event)
    db.commit()
    return None

# 6. PATCH (Update)
@router.patch("/{id}", response_model=schemas.Event)
async def update_event(
    id: int, 
    title: Optional[str] = Form(None),
    description: Optional[str] = Form(None),
    date: Optional[date] = Form(None),
    location: Optional[str] = Form(None),
    file: Optional[UploadFile] = File(None),
    db: Session = Depends(get_db)
):
    event = db.query(models.Event).filter(models.Event.id == id).first()
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")
        
    if title: event.title = title
    if description: event.description = description
    if date: event.date = date
    if location: event.location = location
    
    # Handle File Replacement
    if file:
        # Delete old file
        if os.path.exists(event.flyer_url):
            os.remove(event.flyer_url)
            
        # Save new file
        file.filename = f"{uuid.uuid4()}.jpg"
        contents = await file.read()
        with open(f"{IMAGEDIR}{file.filename}", "wb") as f:
            f.write(contents)
        event.flyer_url = f"{IMAGEDIR}{file.filename}"
        
    db.commit()
    db.refresh(event)
    return event