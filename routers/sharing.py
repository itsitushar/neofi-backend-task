from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from db.session import SessionLocal
from models.shared_access import SharedAccess
from schemas.shared_access import ShareRequest
from models.user import User
from models.event import Event
from core.auth import get_current_user
from schemas.user import PermissionUpdate
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


@router.get("/{id}/permissions")
def get_event_permissions(
    id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # Only owners can see permissions
    event = db.query(Event).filter(Event.id == id).first()
    if not event or event.created_by != current_user.id:
        raise HTTPException(
            status_code=403, detail="Only owners can view permissions")

    shared = db.query(SharedAccess).filter(SharedAccess.event_id == id).all()
    return [
        {
            "user_id": s.user_id,
            "role": s.role
        } for s in shared
    ]


@router.put("/{id}/permissions/{user_id}")
def update_permission(
    id: int,
    user_id: int,
    update: PermissionUpdate,
    role: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    role = update.role
    if role not in ["viewer", "editor"]:
        raise HTTPException(status_code=400, detail="Invalid role")

    event = db.query(Event).filter(Event.id == id).first()
    if not event or event.created_by != current_user.id:
        raise HTTPException(
            status_code=403, detail="Only owners can update permissions")

    access = db.query(SharedAccess).filter(
        SharedAccess.event_id == id,
        SharedAccess.user_id == user_id
    ).first()

    if not access:
        raise HTTPException(
            status_code=404, detail="User does not have access")

    access.role = role
    db.commit()
    return {"message": "Role updated successfully"}


@router.delete("/{id}/permissions/{user_id}")
def remove_permission(
    id: int,
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    event = db.query(Event).filter(Event.id == id).first()
    if not event or event.created_by != current_user.id:
        raise HTTPException(
            status_code=403, detail="Only owners can remove access")

    access = db.query(SharedAccess).filter(
        SharedAccess.event_id == id,
        SharedAccess.user_id == user_id
    ).first()

    if not access:
        raise HTTPException(
            status_code=404, detail="User does not have access")

    db.delete(access)
    db.commit()
    return {"message": "Access removed successfully"}
