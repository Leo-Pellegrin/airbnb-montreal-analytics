from datetime import date
from typing import Optional
from sqlmodel import SQLModel, Field

class Neighbourhoods(SQLModel, table=True):
    neighbourhood: str = Field(primary_key=True)

    model_config = {"table_name": "neighbourhoods"}
