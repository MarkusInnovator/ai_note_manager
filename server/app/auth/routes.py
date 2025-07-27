from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import SessionLocal
from ..models import User
from .schemas import RegisterRequest, LoginRequest, TokenResponse
from .utils import hash_password, verify_password
from .tokens import create_access_token, create_refresh_token
import jwt

router = APIRouter(prefix="/auth", tags=["auth"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/register", response_model=TokenResponse)
def register(data: RegisterRequest, db: Session = Depends(get_db)):
    if db.query(User).filter(User.email == data.email).first():
        raise HTTPException(status_code=400, detail="Email already registered")
    user = User(email=data.email, hashed_password=hash_password(data.password))
    db.add(user)
    db.commit()
    db.refresh(user)
    return {
        "access_token": create_access_token({"sub": user.email}),
        "refresh_token": create_refresh_token({"sub": user.email}),
    }

@router.post("/login", response_model=TokenResponse)
def login(data: LoginRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == data.email).first()
    if not user or not verify_password(data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    return {
        "access_token": create_access_token({"sub": user.email}),
        "refresh_token": create_refresh_token({"sub": user.email}),
    }

@router.post("/refresh", response_model=TokenResponse)
def refresh(token: str):
    # In echter App: decode & verify refresh token, check blacklist
    payload = jwt.decode(token, "secret", algorithms=["HS256"])
    email = payload.get("sub")
    return {
        "access_token": create_access_token({"sub": email}),
        "refresh_token": create_refresh_token({"sub": email}),
    }
