from typing import Optional

from pydantic import EmailStr
from sqlmodel import Field, SQLModel


class User(SQLModel, table=True):
    """
    Table utilisateur
    """

    id: Optional[int] = Field(default=None, primary_key=True)
    email: EmailStr = Field(index=True, nullable=False)
    username: str = Field(index=True, nullable=False)
    password_hash: str = Field(nullable=False)
    full_name: Optional[str] = Field(default=None)
    is_active: bool = Field(default=True)
    is_superuser: bool = Field(default=False)


class UserCreate(SQLModel):
    """
    Schéma pour la création d'un utilisateur
    Contient le mot de passe en clair
    """

    email: EmailStr
    username: str
    password: str
    full_name: Optional[str] = None


class UserRead(SQLModel):
    """
    Schéma en lecture pour un utilisateur
    Sans le hash du mot de passe
    """

    id: int
    email: EmailStr
    username: str
    full_name: Optional[str]
    is_active: bool
    is_superuser: bool

    model_config = {"from_attributes": True}


class UserUpdate(SQLModel):
    """
    Schéma de mise à jour d'un utilisateur
    Tous les champs sont optionnels
    """

    email: Optional[EmailStr] = None
    username: Optional[str] = None
    password: Optional[str] = None
    full_name: Optional[str] = None
    is_active: Optional[bool] = None
    is_superuser: Optional[bool] = None
