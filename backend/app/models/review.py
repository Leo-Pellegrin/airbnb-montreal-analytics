from datetime import date
from typing import Optional

from sqlmodel import Field, SQLModel


class Reviews(SQLModel, table=True):
    """
    Table des avis
    """

    id: Optional[int] = Field(default=None, primary_key=True)
    listing_id: int = Field(foreign_key="listings.id", index=True)
    date: date
    reviewer_id: Optional[int] = Field(default=None)
    reviewer_name: Optional[str] = Field(default=None)
    comments: str


class ReviewRead(SQLModel):
    """
    Schéma en lecture d'un avis
    """

    id: int
    listing_id: int
    date: date
    reviewer_id: Optional[int]
    reviewer_name: Optional[str]
    comments: str

    model_config = {"from_attributes": True}
