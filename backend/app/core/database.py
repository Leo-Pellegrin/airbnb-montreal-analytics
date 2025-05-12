from sqlmodel import Session, SQLModel, create_engine

from app.core.config import settings

engine = create_engine(settings.database_url, echo=False)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)  # crée toutes les tables


def get_session():
    with Session(engine) as session:
        yield session
