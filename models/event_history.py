from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from db.session import Base
from datetime import datetime


class EventHistory(Base):
    __tablename__ = "event_history"

    id = Column(Integer, primary_key=True, index=True)
    event_id = Column(Integer, ForeignKey("events.id"))
    changed_by = Column(Integer, ForeignKey("users.id"))
    change_time = Column(DateTime, default=datetime.utcnow)
    previous_data = Column(Text)

    event = relationship("Event", back_populates="history")
    user = relationship("User")
