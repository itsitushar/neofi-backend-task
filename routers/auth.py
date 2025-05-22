from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from db.session import SessionLocal
from schemas.user import UserCreate, UserOut
from models.user import User
from passlib.context import CryptContext
from core.security import get_password_hash
from fastapi.security import OAuth2PasswordRequestForm
from core.security import verify_password, create_access_token
from datetime import timedelta
from core.config import settings
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from core.security import create_refresh_token

router = APIRouter()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_password_hash(password: str):
    return pwd_context.hash(password)


@router.post("/register", response_model=UserOut)
def register(user: UserCreate, db: Session = Depends(get_db)):
    if db.query(User).filter(User.email == user.email).first():
        raise HTTPException(
            status_code=400, message="Email already registered")
    if db.query(User).filter(User.username == user.username).first():
        raise HTTPException(status_code=400, message="Username already taken")

    new_user = User(
        username=user.username,
        email=user.email,
        hashed_password=get_password_hash(user.password),
        role=user.role
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")


@router.post("/refresh")
def refresh_token(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, settings.SECRET_KEY,
                             algorithms=[settings.ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=401, detail="Invalid token")

        # issue new access token
        new_token = create_access_token(data={"sub": username})
        return {"access_token": new_token, "token_type": "bearer"}

    except JWTError:
        raise HTTPException(status_code=401, detail="Could not refresh token")


@router.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == form_data.username).first()
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=401, message="Invalid credentials")

    access_token = create_access_token(data={"sub": user.username})

    refresh_token = create_refresh_token(data={"sub": user.username})  # new

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer"
    }


@router.post("/logout")
def logout():
    return {"message": "Logged out successfully"}
