# backend/app/api/v1/endpoints/health.py

from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select

from app.core.database import get_session

router = APIRouter()


@router.get("/health", tags=["system"])
def health(session: Session = Depends(get_session)):
    """
    Vérifie la connexion à la BD en sélectionnant littéralement 1.
    """
    try:
        # select(1) crée une requête "SELECT 1"
        result = session.exec(select(1)).one()  # renvoie l'entier 1
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"DB error: {e}")
    return {"status": "ok", "db": result}
