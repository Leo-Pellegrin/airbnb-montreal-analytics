from sqlmodel import SQLModel, create_engine, Session
from app.core.config import settings

# Crée l'engine Postgres
engine = create_engine(
    settings.PGURL, 
    echo=False, 
)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)  # crée toutes les tables

def get_session():
    with Session(engine) as session:
        yield session