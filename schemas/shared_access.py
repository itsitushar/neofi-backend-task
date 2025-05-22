from pydantic import BaseModel
from enum import Enum


class Role(str, Enum):
    owner = "owner"
    editor = "editor"
    viewer = "viewer"


class ShareRequest(BaseModel):
    event_id: int
    user_id: int
    role: Role
