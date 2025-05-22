from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from db.session import Base


class Event(Base):
    __tablename__ = "events"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(String)
    timestamp = Column(DateTime, nullable=False)
    created_by = Column(Integer, ForeignKey("users.id"))

    creator = relationship("User", back_populates="events")
    shared_with = relationship("SharedAccess", back_populates="event")
    history = relationship("EventHistory", back_populates="event")
