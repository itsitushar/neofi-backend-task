from sqlalchemy import Column, Integer, String, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from db.session import Base


class SharedAccess(Base):
    __tablename__ = "shared_access"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    event_id = Column(Integer, ForeignKey("events.id"))
    role = Column(String, nullable=False)  # "owner", "editor", "viewer"

    user = relationship("User", back_populates="shared_events")
    event = relationship("Event", back_populates="shared_with")

    __table_args__ = (
        UniqueConstraint("user_id", "event_id", name="user_event_unique"),
    )
