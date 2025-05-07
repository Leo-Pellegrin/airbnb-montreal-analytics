from typing import Optional
from sqlmodel import SQLModel, Field

class Listings(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    price: float
    latitude: float
    longitude: float
    neighbourhood: str = Field(index=True)
    room_type: str