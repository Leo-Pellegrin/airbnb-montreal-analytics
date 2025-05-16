from sqlmodel import Field, SQLModel
from sqlalchemy import Column, Text


class Neighbourhoods(SQLModel, table=True):
    neighbourhood: str = Field(sa_column=Column(Text, primary_key=True))
    model_config = {"table_name": "neighbourhoods"}
