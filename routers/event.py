from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from db.session import SessionLocal
from models.event import Event
from schemas.event import EventCreate, EventOut, EventUpdate, EventBatchCreate
from core.auth import get_current_user
from models.user import User
from core.permissions import get_user_event_role
from models.EventHistory import EventHistory
import json

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# POST /api/events


@router.post("/", response_model=EventOut)
def create_event(
    event: EventCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    new_event = Event(
        title=event.title,
        description=event.description,
        timestamp=event.timestamp,
        created_by=current_user.id
    )
    db.add(new_event)
    db.commit()
    db.refresh(new_event)
    return new_event

# POST /api/events/batch


@router.post("/batch", response_model=list[EventOut])
def create_multiple_events(
    batch: EventBatchCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    new_events = [
        Event(
            title=e.title,
            description=e.description,
            timestamp=e.timestamp,
            created_by=current_user.id
        ) for e in batch.events
    ]
    db.add_all(new_events)
    db.commit()
    return new_events


@router.get("/", response_model=list[EventOut])
def get_events(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    events = db.query(Event).filter(Event.created_by == current_user.id).all()
    return events


# GET /api/events/{id}


@router.get("/{id}", response_model=EventOut)
def get_event_by_id(
    id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    role = get_user_event_role(current_user, id, db)
    if role is None:
        raise HTTPException(status_code=403, message="Access denied")

    event = db.query(Event).filter(Event.id == id).first()
    return event

# PUT /api/events/{id}


@router.put("/{id}", response_model=EventOut)
def update_event(
    id: int,
    updates: EventUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    role = get_user_event_role(current_user, id, db)
    if role not in ["owner", "editor"]:
        raise HTTPException(status_code=403, message="No edit access")

    event = db.query(Event).filter(Event.id == id).first()
    if not event:
        raise HTTPException(status_code=404, message="Event not found")

    event_data = {
        "title": event.title,
        "description": event.description,
        "timestamp": event.timestamp.isoformat()
    }

    history = EventHistory(
        event_id=event.id,
        changed_by=current_user.id,
        previous_data=json.dumps(event_data)
    )
    db.add(history)
    for field, value in updates.dict(exclude_unset=True).items():
        setattr(event, field, value)
    db.commit()
    db.refresh(event)
    return event

# DELETE /api/events/{id}


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_event(
    id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    role = get_user_event_role(current_user, id, db)
    if role != "owner":
        raise HTTPException(status_code=403, message="Only owners can delete")

    event = db.query(Event).filter(Event.id == id).first()
    if not event:
        raise HTTPException(status_code=404, message="Event not found")

    db.delete(event)
    db.commit()


@router.get("/{id}/history")
def get_event_history(
    id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    role = get_user_event_role(current_user, id, db)
    if role not in ["owner", "editor", "viewer"]:
        raise HTTPException(status_code=403, message="Access denied")

    history = db.query(EventHistory).filter(EventHistory.event_id == id).all()
    return [
        {
            "change_time": h.change_time,
            "changed_by": h.changed_by,
            "previous_data": json.loads(h.previous_data)
        } for h in history
    ]
