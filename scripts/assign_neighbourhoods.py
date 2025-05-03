#!/usr/bin/env python3
"""
assign_neighbourhoods.py
------------------------
Complète la colonne `neighbourhood` manquante de listings_clean.csv
à partir des polygones neighbourhoods.geojson.
"""

import pandas as pd
import geopandas as gpd
from shapely.geometry import Point
from pathlib import Path

DATA_DIR = Path("./clean")

# 1) charger les polygones
gdf_neigh = gpd.read_file("./dataset/neighbourhoods.geojson")
gdf_neigh = gdf_neigh[["neighbourhood", "geometry"]]   # garde l'essentiel
gdf_neigh = gdf_neigh.to_crs("EPSG:4326")               # WGS‑84 (lat/lon)

# 2) charger listings_clean
df = pd.read_csv(DATA_DIR / "listings_clean.csv")
mask_missing = df["neighbourhood"].isna()
df_missing   = df.loc[mask_missing].copy()

# 3) convertir points -> GeoDataFrame
gdf_points = gpd.GeoDataFrame(
    df_missing,
    geometry=[Point(xy) for xy in zip(df_missing["longitude"], df_missing["latitude"])],
    crs="EPSG:4326"
)

# 4) jointure spatiale (point in polygon)
joined = gpd.sjoin(gdf_points, gdf_neigh, how="left", predicate="within")

# 5) Mise à jour : s'il y a un quartier, on le remplit ; sinon "Unknown"
df.loc[mask_missing, "neighbourhood"] = joined["neighbourhood_right"].fillna("Unknown")

# 6) sauvegarde
out_path = DATA_DIR / "listings_clean_geo.csv"
df.drop(columns="geometry", errors="ignore").to_csv(out_path, index=False)
print(f"✅  listings_clean_geo.csv généré ({out_path})")

df = pd.read_csv("./clean/listings_clean_geo.csv")
print("quartiers manquants :", df["neighbourhood"].isna().sum())  
print(df["neighbourhood"].value_counts(dropna=False).head())

df = pd.read_csv("./clean/listings_clean_geo.csv")
mask = df["neighbourhood"] == "Neighborhood highlights"
df.loc[mask, "neighbourhood"] = "Unknown"   
df.to_csv("./clean/listings_clean_geo.csv", index=False)