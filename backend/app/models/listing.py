from typing import Optional

from sqlmodel import Field, SQLModel


class Listings(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    price: float
    latitude: float
    longitude: float
    neighbourhood: str = Field(foreign_key="neighbourhoods.neighbourhood")
    room_type: str
