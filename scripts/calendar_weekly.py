#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pandas as pd
import gzip

def clean_price(price_str):
    """Clean price string by removing '$' and converting to float."""
    if pd.isna(price_str):
        return None
    # Take the first price if multiple prices are concatenated
    price_str = str(price_str).split('$')[1].split('$')[0]
    # Remove commas from the price string
    price_str = price_str.replace(',', '')
    return float(price_str)

def build_calendar_weekly(
    input_csv: str  = "dataset/calendar.csv.gz",
    output_csv: str = "clean/calendar_weekly_clean.csv",
):
    """
    Lit le CSV de calendar (jour par jour), agrège par semaine et par listing,
    et écrit un fichier CSV avec 4 colonnes : listing_id, week_id, avg_price, occupancy_pct.
    """

    # 1) Lecture du fichier et parsing de la date
    # Détection si le fichier est gzippé
    if input_csv.endswith('.gz'):
        df = pd.read_csv(input_csv, compression='gzip', parse_dates=["date"], low_memory=False)
    else:
        df = pd.read_csv(input_csv, parse_dates=["date"], low_memory=False)

    # Clean price column
    df['price'] = df['price'].apply(clean_price)

    # Si available est en 't'/'f', on convertit en bool
    if df["available"].dtype == object:
        df["available"] = df["available"].map({"t": True, "f": False})

    # 2) Calcul de l'identifiant de semaine : lundi de chaque semaine
    #    .dt.to_period("W") donne la période du dimanche à samedi
    #    On utilise maintenant la méthode to_timestamp() au lieu de start_time
    df["week_id"] = (
        df["date"]
        .dt.to_period("W-SUN")    # semaines commençant le dimanche
        .apply(lambda p: p.to_timestamp().date())
    )

    # 3) Agrégation
    weekly = (
        df
        .groupby(["listing_id", "week_id"], as_index=False)
        .agg(
            avg_price      = ("price", "mean"),
            occupancy_pct  = ("available", lambda x: (~x).astype(int).mean())  # Inverser available pour obtenir l'occupation
        )
    )

    # 4) Arrondi et formatage
    weekly["avg_price"]     = weekly["avg_price"].round(2)
    weekly["occupancy_pct"] = weekly["occupancy_pct"].round(4)  # Garder en décimal (0-1)

    # 5) Export
    weekly.to_csv(output_csv, index=False)
    print(f"✅ '{output_csv}' généré ({len(weekly)} lignes).")

if __name__ == "__main__":
    build_calendar_weekly()