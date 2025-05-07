from typing import List, Optional
from fastapi import APIRouter, Depends, Query, HTTPException
from sqlmodel import Session, select
from app.core.database import get_session
from app.models.listing import Listing
from app.models.review import ReviewRead, Review

router = APIRouter()

@router.get(
    "/listings",
    response_model=List[Listing],
    tags=["listings"],
)
def read_listings(
    *,
    limit: int = Query(20, ge=1, le=100, description="Nombre max de résultats"),
    offset: int = Query(0, ge=0, description="Décalage pour la pagination"),
    room_type: Optional[str]  = Query(None, description="Type de logement"),
    price_max: Optional[float] = Query(None, ge=0, description="Prix max"),
    session: Session = Depends(get_session),
):
    """
    Récupère une liste paginée de listings, optionnellement filtrée.
    """
    query = select(Listing)
    if room_type:
        query = query.where(Listing.room_type == room_type)
    if price_max is not None:
        query = query.where(Listing.price <= price_max)
    query = query.limit(limit).offset(offset)

    results = session.exec(query).all()
    if results is None:
        raise HTTPException(status_code=404, detail="No listings found")
    return results

@router.get(
    "/listings/{id}",
    response_model=Listing,
    tags=["listings"],
)
def read_listing(id: int, session: Session = Depends(get_session)):
    listing = session.get(Listing, id)
    if not listing:
        raise HTTPException(404, "Listing not found")
    return listing

@router.get(
    "/listings/{id}/reviews",
    response_model=List[ReviewRead],
    tags=["reviews"],
)
def read_reviews_for_listing(
    id: int,
    session: Session = Depends(get_session),
):
    stmt = select(Review).where(Review.listing_id == id)
    return session.exec(stmt).all()