from pydantic import BaseModel
from datetime import datetime


class EventBase(BaseModel):
    title: str
    description: str
    timestamp: datetime


class EventCreate(EventBase):
    pass


class EventBatchCreate(BaseModel):
    events: list[EventCreate]


class EventUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    timestamp: datetime | None = None


class EventOut(EventBase):
    id: int
    created_by: int

    class Config:
        orm_mode = True
