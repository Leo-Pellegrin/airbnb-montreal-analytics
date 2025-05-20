# backend/app/api/v1/endpoints/stats.py

from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select, text

from app.core.database import get_session
from app.models.neighbourhoods import Neighbourhoods
from app.models.stats import StatsOut

router = APIRouter()


@router.get(
    "/stats/median_price",
    response_model=int,
    tags=["stats"],
)
async def stats_median_price(
    session: Session = Depends(get_session),
):
    """
    Médiane des prix des listings pour tous les quartiers.
    """
    stmt = text(
        """
        WITH latest AS (
          SELECT MAX(week_id) AS week_id
          FROM calendar_weekly
        )
        SELECT percentile_cont(0.5) WITHIN GROUP (ORDER BY avg_price) AS median_price
        FROM calendar_weekly
        JOIN listings ON calendar_weekly.listing_id = listings.id
        JOIN latest ON calendar_weekly.week_id = latest.week_id
        """
    )
    result = session.exec(stmt).first()
    if result is None or result._mapping["median_price"] is None:
        raise HTTPException(
            status_code=404,
            detail="Aucune donnée disponible pour le calcul de la médiane des prix",
        )
    return result._mapping["median_price"]


@router.get(
    "/stats/occupancy_pct",
    response_model=float,
    tags=["stats"],
)
async def stats_occupancy_pct(
    session: Session = Depends(get_session),
):
    """
    Moyenne des taux d'occupation pour tous les quartiers.
    """
    stmt = text(
        """
        WITH latest AS (
          SELECT MAX(week_id) AS week_id
          FROM calendar_weekly
        )
        SELECT AVG(occupancy_pct) AS occupancy_pct
        FROM calendar_weekly
        JOIN listings ON calendar_weekly.listing_id = listings.id
        JOIN latest ON calendar_weekly.week_id = latest.week_id
        """
    )
    result = session.exec(stmt).first()
    if result is None or result._mapping["occupancy_pct"] is None:
        raise HTTPException(
            status_code=404,
            detail="Aucune donnée disponible pour le calcul de la moyenne des taux d'occupation",
        )
    return result._mapping["occupancy_pct"]


@router.get(
    "/stats/avg_sentiment",
    response_model=float,
    tags=["stats"],
)
async def stats_avg_sentiment(
    session: Session = Depends(get_session),
):
    from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

    sia = SentimentIntensityAnalyzer()

    def vader_score(text: str) -> float:
        return sia.polarity_scores(text)["compound"]

    """
    Moyenne des sentiments pour tous les quartiers.
    """
    stmt = text(
        """
        SELECT comments
        FROM reviews
        WHERE comments IS NOT NULL
        """
    )
    results = session.exec(stmt).all()

    if not results:
        raise HTTPException(
            status_code=404,
            detail="Aucune donnée disponible pour le calcul de la moyenne des sentiments",
        )

    # Calculer le sentiment pour chaque commentaire
    sentiments = [vader_score(review.comments) for review in results]

    # Calculer la moyenne
    avg_sentiment = sum(sentiments) / len(sentiments)

    return avg_sentiment


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
        raise HTTPException(
            status_code=404, detail="Aucune donnée disponible pour ce quartier"
        )
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
