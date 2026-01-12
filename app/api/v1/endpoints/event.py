from fastapi import APIRouter, Depends, HTTPException, Query, UploadFile, File, Form
from sqlalchemy.orm import Session
from sqlalchemy import or_
from typing import List, Optional
from datetime import datetime
from app.api import deps
from app.models.event import Event
from app.models.user import User
from app.schemas.event import EventOut, EventUpdate

router = APIRouter()

# 1. POST /events/ (Auth Required + File Upload)
@router.post("/", response_model=EventOut)
async def create_event(
    title: str = Form(...),
    description: str = Form(None),
    start_time: str = Form(...),
    location: str = Form(None),
    capacity: int = Form(100),
    is_public: bool = Form(True),
    flyer: Optional[UploadFile] = File(None),
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user)
):
    # Logic to save flyer to disk/cloud would go here
    flyer_path = f"uploads/{flyer.filename}" if flyer else None
    
    new_event = Event(
        title=title,
        description=description,
        start_time=datetime.fromisoformat(start_time),
        location=location,
        capacity=capacity,
        is_public=is_public,
        owner_id=current_user.id,
        flyer_url=flyer_path
    )
    db.add(new_event)
    db.commit()
    db.refresh(new_event)
    return new_event

# 2. GET /events/ (Filters + Pagination)
@router.get("/", response_model=List[EventOut])
def list_events(
    q: Optional[str] = None,
    location: Optional[str] = None,
    from_date: Optional[datetime] = None,
    to_date: Optional[datetime] = None,
    is_public: Optional[bool] = Query(None),
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(deps.get_db)
):
    query = db.query(Event)
    
    if q:
        query = query.filter(or_(Event.title.contains(q), Event.description.contains(q)))
    if location:
        query = query.filter(Event.location == location)
    if from_date:
        query = query.filter(Event.start_time >= from_date)
    if to_date:
        query = query.filter(Event.start_time <= to_date)
    if is_public is not None:
        query = query.filter(Event.is_public == is_public)
        
    return query.offset(skip).limit(limit).all()

# 3. GET /events/{event_id}
@router.get("/{event_id}", response_model=EventOut)
def get_event(event_id: int, db: Session = Depends(deps.get_db)):
    event = db.query(Event).filter(Event.id == event_id).first()
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")
    return event

# 4. PATCH /events/{event_id} (Organizer Only)
@router.patch("/{event_id}", response_model=EventOut)
def update_event(
    event_id: int,
    event_in: EventUpdate,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user)
):
    db_event = db.query(Event).filter(Event.id == event_id).first()
    if not db_event:
        raise HTTPException(status_code=404, detail="Event not found")
    if db_event.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to edit this event")
    
    for field, value in event_in.model_dump(exclude_unset=True).items():
        setattr(db_event, field, value)
    
    db.commit()
    db.refresh(db_event)
    return db_event

# 5. DELETE /events/{event_id} (Organizer/Admin Only)
@router.delete("/{event_id}", status_code=204)
def delete_event(
    event_id: int,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user)
):
    db_event = db.query(Event).filter(Event.id == event_id).first()
    if not db_event:
        raise HTTPException(status_code=404, detail="Event not found")
    if db_event.owner_id != current_user.id and not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Not authorized")
    
    db.delete(db_event)
    db.commit()
    return None