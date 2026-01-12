from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.api import deps
from app.models.event import Event
from app.models.rsvp import RSVP
from app.models.user import User
from app.schemas.rsvp import RSVPCreate, RSVPOut, RSVPStatus

router = APIRouter()

# 1. POST /events/{event_id}/rsvp
@router.post("/{event_id}/rsvp", response_model=RSVPOut)
def create_or_update_rsvp(
    event_id: int, 
    rsvp_in: RSVPCreate,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user)
):
    event = db.query(Event).filter(Event.id == event_id).first()
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")

    # Enforce Capacity Check
    if rsvp_in.status == RSVPStatus.going:
        current_attendees = db.query(RSVP).filter(
            RSVP.event_id == event_id, 
            RSVP.status == RSVPStatus.going
        ).count()
        if event.capacity and current_attendees >= event.capacity:
            raise HTTPException(status_code=400, detail="Event is at full capacity")

    # Check if RSVP exists (Update if it does, Create if not)
    db_rsvp = db.query(RSVP).filter(
        RSVP.event_id == event_id, 
        RSVP.user_id == current_user.id
    ).first()

    if db_rsvp:
        db_rsvp.status = rsvp_in.status
    else:
        db_rsvp = RSVP(event_id=event_id, user_id=current_user.id, status=rsvp_in.status)
        db.add(db_rsvp)
    
    db.commit()
    db.refresh(db_rsvp)
    return db_rsvp

# 2. GET /events/{event_id}/rsvps (Organizer/Admin only)
@router.get("/{event_id}/rsvps", response_model=List[RSVPOut])
def get_event_rsvps(
    event_id: int,
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user)
):
    event = db.query(Event).filter(Event.id == event_id).first()
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")
    
    # Simple check: only the creator can see the full list
    if event.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Only the organizer can view all RSVPs")

    return db.query(RSVP).filter(RSVP.event_id == event_id).offset(skip).limit(limit).all()

# 3. GET /events/{event_id}/rsvps/me
@router.get("/{event_id}/rsvps/me", response_model=RSVPOut)
def get_my_rsvp(
    event_id: int,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user)
):
    rsvp = db.query(RSVP).filter(RSVP.event_id == event_id, RSVP.user_id == current_user.id).first()
    if not rsvp:
        raise HTTPException(status_code=404, detail="You have not RSVP'd to this event")
    return rsvp

# 4. DELETE /events/{event_id}/rsvp
@router.delete("/{event_id}/rsvp", status_code=status.HTTP_204_NO_CONTENT)
def delete_rsvp(
    event_id: int,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user)
):
    db_rsvp = db.query(RSVP).filter(RSVP.event_id == event_id, RSVP.user_id == current_user.id).first()
    if not db_rsvp:
        raise HTTPException(status_code=404, detail="RSVP not found")
    
    db.delete(db_rsvp)
    db.commit()
    return None