# backend/app/models/stats.py

from sqlmodel import SQLModel, Field

class StatsOut(SQLModel):
    median_price: float = Field(..., description="Prix médian (CAD)")
    occupancy_pct: float = Field(..., description="Taux d'occupation (0–1)")
    avg_sentiment: float = Field(..., description="Score moyen de sentiment")

    model_config = {"from_attributes": True}