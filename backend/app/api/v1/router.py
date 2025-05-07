from fastapi import APIRouter
from .endpoints import listings, stats, health, neighbourhoods, auth

api_router = APIRouter()

api_router.include_router(listings.router, tags=["listings"])
api_router.include_router(stats.router,    tags=["stats"])
api_router.include_router(health.router,    tags=["health"])
api_router.include_router(neighbourhoods.router, tags=["neighbourhoods"])
api_router.include_router(auth.router, tags=["auth"])