from sqlalchemy.orm import Session
from models.shared_access import SharedAccess
from models.event import Event
from models.user import User


def get_user_event_role(user: User, event_id: int, db: Session) -> str | None:
    # Owner check
    event = db.query(Event).filter(Event.id == event_id).first()
    if event and event.created_by == user.id:
        return "owner"

    # Shared access check
    shared = db.query(SharedAccess).filter(
        SharedAccess.user_id == user.id,
        SharedAccess.event_id == event_id
    ).first()

    if shared:
        return shared.role

    return None  # No access
