# backend/app/api/v1/endpoints/users.py

from fastapi import APIRouter, Depends, HTTPException, status
from passlib.context import CryptContext
from sqlmodel import Session

from app.core.auth import get_current_user
from app.core.database import get_session
from app.models.user import User, UserCreate, UserRead, UserUpdate

pwd_ctx = CryptContext(schemes=["bcrypt"], deprecated="auto")

router = APIRouter(prefix="/users", tags=["users"])


@router.post("/", response_model=UserRead, status_code=status.HTTP_201_CREATED)
def create_user(payload: UserCreate, session: Session = Depends(get_session)):
    hashed_password = pwd_ctx.hash(payload.password)
    user = User(
        email=payload.email,
        username=payload.username,
        password_hash=hashed_password,
        full_name=payload.full_name,
    )
    session.add(user)
    session.commit()
    session.refresh(user)
    return user


@router.get(
    "/{user_id}", response_model=UserRead, dependencies=[Depends(get_current_user)]
)
def read_user(user_id: int, session: Session = Depends(get_session)):
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "User not found")
    return user


@router.put("/{user_id}", response_model=UserRead)
def update_user(
    user_id: int, payload: UserUpdate, session: Session = Depends(get_session)
):
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "User not found")
    user_data = payload.model_dump(exclude_unset=True)
    for k, v in user_data.items():
        setattr(user, k, v)
    session.add(user)
    session.commit()
    session.refresh(user)
    return user


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(user_id: int, session: Session = Depends(get_session)):
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "User not found")
    session.delete(user)
    session.commit()
