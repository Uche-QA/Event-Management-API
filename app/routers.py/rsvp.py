from typing import List

# Database and Core logic
from app.database import get_db
from app.models.event import Event
from app.models.rsvp import RSVP
from app.schemas.event import Event as EventSchema
from app.schemas.rsvp import RSVPCreate, RSVP as RSVPSchema

# We don't use a prefix here because the paths vary
router = APIRouter(tags=["RSVPs"])

# 1. POST (RSVP to an Event)
@router.post("/events/{event_id}/rsvp", response_model=schemas.RSVP)
def create_rsvp(event_id: int, rsvp: schemas.RSVPCreate, db: Session = Depends(get_db)):
    # Check if event exists first
    event = db.query(models.Event).filter(models.Event.id == event_id).first()
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")
    
    new_rsvp = models.RSVP(**rsvp.dict(), event_id=event_id)
    db.add(new_rsvp)
    db.commit()
    db.refresh(new_rsvp)
    return new_rsvp

# 2. GET (List guests for an Event)
@router.get("/events/{event_id}/rsvps", response_model=List[schemas.RSVP])
def read_rsvps(event_id: int, db: Session = Depends(get_db)):
    rsvps = db.query(models.RSVP).filter(models.RSVP.event_id == event_id).all()
    return rsvps

# 3. DELETE (Cancel RSVP)
@router.delete("/rsvps/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_rsvp(id: int, db: Session = Depends(get_db)):
    rsvp = db.query(models.RSVP).filter(models.RSVP.id == id).first()
    if not rsvp:
        raise HTTPException(status_code=404, detail="RSVP not found")
    
    db.delete(rsvp)
    db.commit()
    return None