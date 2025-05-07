# backend/app/api/v1/endpoints/auth.py

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from passlib.context import CryptContext
from app.core.database import get_session
from sqlmodel import Session, select
from app.core.auth import create_access_token  # votre utilitaire JWT
from app.models.user import User, UserCreate, UserRead

router = APIRouter(tags=["auth"])
pwd_ctx = CryptContext(schemes=["bcrypt"], deprecated="auto")

class LoginIn(BaseModel):
    email: str
    password: str

class TokenOut(BaseModel):
    access_token: str
    token_type: str = "bearer"

@router.post("/login", response_model=TokenOut)
def login(data: LoginIn, session: Session = Depends(get_session)):
    stmt = select(User).where(User.email == data.email)
    user = session.exec(stmt).first()
    if not user or not pwd_ctx.verify(data.password, user.password_hash):
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Invalid credentials")
    token = create_access_token(sub=user.id)
    return {"access_token": token}


