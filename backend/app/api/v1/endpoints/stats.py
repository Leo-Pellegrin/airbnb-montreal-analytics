# backend/app/api/v1/endpoints/stats.py

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlmodel import Session, text
from typing import List
from app.core.database import get_session
from app.models.stats import StatsOut

router = APIRouter()

@router.get(
    "/stats/{neigh}",
    response_model=StatsOut,
    tags=["stats"],
)
def stats_by_neigh(
    neigh: str,
    session: Session = Depends(get_session),
):
    """
    Récupère pour le quartier `neigh` les KPI (prix médian, taux d'occupation,
    sentiment) pour la dernière semaine disponible.
    """
    stmt = text(
        """
        SELECT
          median_price,
          occupancy_pct,
          avg_sentiment
        FROM calendar_weekly_neigh
        WHERE neighbourhood = :neigh
        ORDER BY week_id DESC
        LIMIT 1
        """
    )
    result = session.exec(stmt.bindparams(neigh=neigh)).first()
    if not result:
        raise HTTPException(status_code=404, detail="Neighbourhood not found")
    # result._mapping contient un dict {column: value}
    return StatsOut(**result._mapping)

@router.get(
    "/stats/{neigh}/history",
    response_model=List[StatsOut],
    tags=["stats"],
)
def stats_history(
    neigh: str,
    period: str = Query("weekly", enum=["weekly","monthly"]),
    session: Session = Depends(get_session),
):
    table = "calendar_weekly_neigh" if period=="weekly" else "calendar_monthly_neigh"
    stmt = text(f"""
      SELECT week_id AS period_id, median_price, occupancy_pct, avg_sentiment
      FROM {table}
      WHERE neighbourhood = :neigh
      ORDER BY period_id DESC
      LIMIT 52
    """)
    rows = session.exec(stmt.bindparams(neigh=neigh)).all()
    return [StatsOut(**r._mapping) for r in rows]