
from sqlmodel import Field, SQLModel


class Neighbourhoods(SQLModel, table=True):
    neighbourhood: str = Field(primary_key=True)

    model_config = {"table_name": "neighbourhoods"}
