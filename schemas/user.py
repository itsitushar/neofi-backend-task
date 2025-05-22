from pydantic import BaseModel
from pydantic import BaseModel, EmailStr  # type: ignore


class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str
    role: str = "user"  # 3 types of roles- admin, auditor, user


class UserOut(BaseModel):
    id: int
    username: str
    email: EmailStr
    role: str

    class Config:
        from_attributes = True


class PermissionUpdate(BaseModel):
    role: str
