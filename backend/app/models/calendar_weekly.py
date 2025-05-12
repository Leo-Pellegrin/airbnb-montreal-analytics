from datetime import date
from typing import Optional
from sqlmodel import SQLModel, Field

class calendar_weekly(SQLModel, table=True):
    listing_id: int = Field(foreign_key="listings.id", primary_key=True)
    week_id: date = Field(primary_key=True)
    avg_price: float 
    occupancy_pct: float

    model_config = {"table_name": "calendar_weekly"}




  