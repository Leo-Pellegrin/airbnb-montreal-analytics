from typing import Optional

from sqlmodel import Field, SQLModel


class Role(SQLModel, table=True):
    """
    Table rôle
    """

    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True, unique=True, nullable=False)
    description: Optional[str] = Field(default=None)


class RoleCreate(SQLModel):
    """
    Schéma pour la création d'un rôle
    """

    name: str
    description: Optional[str] = None


class RoleRead(SQLModel):
    """
    Schéma en lecture pour un rôle
    """

    id: int
    name: str
    description: Optional[str]

    model_config = {"from_attributes": True}


class RoleUpdate(SQLModel):
    """
    Schéma de mise à jour d'un rôle
    Tous les champs sont optionnels
    """

    name: Optional[str] = None
    description: Optional[str] = None
