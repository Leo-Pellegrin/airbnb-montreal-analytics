
# backend/app/api/v1/endpoints/roles.py

from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select
from app.core.database import get_session
from app.models.role import Role, RoleCreate, RoleRead, RoleUpdate  # à créer

router = APIRouter(prefix="/roles", tags=["roles"])

@router.post("/", response_model=RoleRead, status_code=status.HTTP_201_CREATED)
def create_role(payload: RoleCreate, session: Session = Depends(get_session)):
    role = Role.model_validate(payload)
    session.add(role)
    session.commit()
    session.refresh(role)
    return role

@router.get("/", response_model=List[RoleRead])
def read_roles(session: Session = Depends(get_session)):
    roles = session.exec(select(Role)).all()
    return roles

@router.get("/{role_id}", response_model=RoleRead)
def read_role(role_id: int, session: Session = Depends(get_session)):
    role = session.get(Role, role_id)
    if not role:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Role not found")
    return role

@router.put("/{role_id}", response_model=RoleRead)
def update_role(role_id: int, payload: RoleUpdate, session: Session = Depends(get_session)):
    role = session.get(Role, role_id)
    if not role:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Role not found")
    role_data = payload.model_dump(exclude_unset=True)
    for k, v in role_data.items():
        setattr(role, k, v)
    session.add(role)
    session.commit()
    session.refresh(role)
    return role

@router.delete("/{role_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_role(role_id: int, session: Session = Depends(get_session)):
    role = session.get(Role, role_id)
    if not role:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Role not found")
    session.delete(role)
    session.commit()