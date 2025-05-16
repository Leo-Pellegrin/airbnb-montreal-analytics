from fastapi import APIRouter

# from app.core.auth import get_current_user  # plus besoin

from .endpoints import health, listings, neighbourhoods, stats

api_router = APIRouter()

api_router.include_router(listings.router, tags=["listings"])
api_router.include_router(stats.router, tags=["stats"])
api_router.include_router(health.router, tags=["health"])
api_router.include_router(neighbourhoods.router, tags=["neighbourhoods"])
