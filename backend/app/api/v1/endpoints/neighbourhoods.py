from typing import List
from fastapi import APIRouter, Depends
from sqlmodel import Session, select, distinct
from app.core.database import get_session
from app.models.listing import Listing

router = APIRouter()

@router.get(
    "/neighbourhoods",
    response_model=List[str],
    tags=["neighbourhoods"],
)
def read_neighbourhoods(session: Session = Depends(get_session)):
    stmt = select(distinct(Listing.neighbourhood))
    return [row[0] for row in session.exec(stmt).all()]