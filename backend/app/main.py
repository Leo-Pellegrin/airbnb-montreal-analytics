from fastapi import FastAPI
from contextlib import asynccontextmanager

from app.core.database import create_db_and_tables
from app.api.v1.router import api_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup : création des tables SQLModel
    create_db_and_tables()
    yield
    # Shutdown : pas de tâche spécifique

app = FastAPI(
    title="Airbnb MTL API",
    version="0.1.0",
    lifespan=lifespan,
)

# Inclusion du routeur de l'API
app.include_router(api_router, prefix="/api/v1")
