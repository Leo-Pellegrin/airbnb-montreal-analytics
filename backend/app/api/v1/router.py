from fastapi import APIRouter, Depends

from app.core.auth import get_current_user

from .endpoints import (auth, health, listings, neighbourhoods, role, stats,
                        users)

api_router = APIRouter()

api_router.include_router(
    listings.router, tags=["listings"], dependencies=[Depends(get_current_user)]
)
api_router.include_router(
    stats.router, tags=["stats"], dependencies=[Depends(get_current_user)]
)
api_router.include_router(
    health.router, tags=["health"], dependencies=[Depends(get_current_user)]
)
api_router.include_router(
    neighbourhoods.router,
    tags=["neighbourhoods"],
    dependencies=[Depends(get_current_user)],
)
api_router.include_router(
    role.router, tags=["role"], dependencies=[Depends(get_current_user)]
)
api_router.include_router(users.router, tags=["users"])
api_router.include_router(auth.router, tags=["auth"])
