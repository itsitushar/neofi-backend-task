from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from db.session import SessionLocal
from models.shared_access import SharedAccess
from schemas.shared_access import ShareRequest
from models.user import User
from models.event import Event
from core.auth import get_current_user

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/share")
def share_event(
    req: ShareRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    event = db.query(Event).filter(Event.id == req.event_id).first()

    if not event or event.created_by != current_user.id:
        raise HTTPException(
            status_code=403, message="Only owner can share this event")

    existing = db.query(SharedAccess).filter(
        SharedAccess.user_id == req.user_id,
        SharedAccess.event_id == req.event_id
    ).first()

    if existing:
        existing.role = req.role  # update role
    else:
        access = SharedAccess(user_id=req.user_id,
                              event_id=req.event_id, role=req.role)
        db.add(access)

    db.commit()
    return {"message": "Shared successfully"}
