from sqlmodel import SQLModel, create_engine, Session
from app.core.config import settings

engine = create_engine(settings.database_url, echo=False)
print(f"🚀 Connexion DB utilisée : {settings.database_url}")

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)  # crée toutes les tables

def get_session():
    with Session(engine) as session:
        yield session