# backend/app/api/v1/endpoints/stats.py

from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, text, select
from typing import List
from app.core.database import get_session
from app.models.stats import StatsOut
from app.models.neighbourhoods import Neighbourhoods

router = APIRouter()

@router.get(
    "/stats/{neigh}",
    response_model=StatsOut,
    tags=["stats"],
)
async def stats_by_neigh(
    neigh: str,
    session: Session = Depends(get_session),
):
    """
    KPI pour le dernier week_id disponible :
      • median_price  = médiane des avg_price
      • occupancy_pct = moyenne des occupancy_pct
    pour tous les listings du quartier `neigh`.
    """
    # Vérifier d'abord si le quartier existe
    neighbourhood = session.exec(
        select(Neighbourhoods).where(Neighbourhoods.neighbourhood == neigh)
    ).first()
    if not neighbourhood:
        raise HTTPException(status_code=404, detail="Quartier non trouvé")

    stmt = text(
        """
        WITH latest AS (
          SELECT MAX(week_id) AS week_id
          FROM calendar_weekly
        )
        SELECT
          percentile_cont(0.5) WITHIN GROUP (ORDER BY cw.avg_price) AS median_price,
          AVG(cw.occupancy_pct)                           AS occupancy_pct
        FROM calendar_weekly cw
        JOIN listings l ON cw.listing_id = l.id
        JOIN latest     ON cw.week_id = latest.week_id
        WHERE l.neighbourhood = :neigh
        """
    )
    result = session.exec(stmt.bindparams(neigh=neigh)).first()
    if result is None or result._mapping["median_price"] is None:
        raise HTTPException(status_code=404, detail="Aucune donnée disponible pour ce quartier")
    return StatsOut(**result._mapping)


@router.get(
    "/stats/{neigh}/history",
    response_model=List[StatsOut],
    tags=["stats"],
)
def stats_history(
    neigh: str,
    session: Session = Depends(get_session),
):
    """
    Historique hebdomadaire des KPI (médiane prix + moyenne occu) 
    par week_id pour le quartier `neigh`, limité aux 52 dernières semaines.
    """
    stmt = text(
        """
        SELECT
          cw.week_id                                    AS period_id,
          percentile_cont(0.5) WITHIN GROUP (ORDER BY cw.avg_price) AS median_price,
          AVG(cw.occupancy_pct)                               AS occupancy_pct
        FROM calendar_weekly cw
        JOIN listings l ON cw.listing_id = l.id
        WHERE l.neighbourhood = :neigh
        GROUP BY cw.week_id
        ORDER BY cw.week_id DESC
        LIMIT 52
        """
    )
    rows = session.exec(stmt.bindparams(neigh=neigh)).all()
    return [StatsOut(**r._mapping) for r in rows]