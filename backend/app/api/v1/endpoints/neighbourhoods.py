from typing import List

from fastapi import APIRouter, Depends
from sqlmodel import Session, select

from app.core.database import get_session
from app.models.neighbourhoods import Neighbourhoods

router = APIRouter()


@router.get(
    "/neighbourhoods",
    response_model=List[str],
    tags=["neighbourhoods"],
)
def read_neighbourhoods(session: Session = Depends(get_session)):
    result = [row.neighbourhood for row in session.exec(select(Neighbourhoods)).all()]
    return result
