
#!/usr/bin/env python3
"""
validate_clean_csv.py
---------------------

Vérifie l'intégrité des fichiers *clean.csv* (Airbnb Montréal) avant import Supabase.

Usage :
    python validate_clean_csv.py ./clean
"""

import sys, pathlib, pandas as pd

DIR = pathlib.Path(sys.argv[1]) if len(sys.argv) > 1 else pathlib.Path("./clean")

def report(title):
    print(f"\n=== {title} ===")

def validate_listings(df):
    report("LISTINGS")
    # 1. unicité id
    dupl = df["id"].duplicated().sum()
    print(f"🗝️ id en double : {dupl}")
    # 2. valeurs manquantes
    print("🔍 Valeurs NaN (cols clés) :")
    for col in ["price", "latitude", "longitude", "neighbourhood"]:
        print(f"  {col:15s} : {df[col].isna().sum()}")
    # 3. bornes
    invalid_lat = df[(df["latitude"] < 40) | (df["latitude"] > 60)]
    invalid_lon = df[(df["longitude"] < -80) | (df["longitude"] > -50)]
    print(f"🌐 Latitude hors [40,60]   : {len(invalid_lat)}")
    print(f"🌐 Longitude hors [-80,-50] : {len(invalid_lon)}")
    # 4. prix négatif
    neg_price = df[df["price"] < 0]
    print(f"💲 Prix négatifs : {len(neg_price)}")

def validate_calendar(df, listings_ids):
    report("CALENDAR")
    # clé composite
    dup = df[["listing_id", "date"]].duplicated().sum()
    print(f"🗝️ (listing_id,date) doublons : {dup}")
    # FK
    unknown = df.loc[~df["listing_id"].isin(listings_ids), "listing_id"].nunique()
    print(f"🔗 listing_id non présent dans listings : {unknown}")
    # prix <0
    neg_price = df[df["price"] < 0]
    print(f"💲 Prix négatifs : {len(neg_price)}")

def validate_reviews(df, listings_ids):
    report("REVIEWS")
    # unicité id
    dup = df["id"].duplicated().sum()
    print(f"🗝️ id en double : {dup}")
    # valeurs manquantes
    missing_comments = df["comments"].isna().sum()
    print(f"💬 Avis sans commentaire : {missing_comments}")
    # FK
    unknown = df.loc[~df["listing_id"].isin(listings_ids), "listing_id"].nunique()
    print(f"🔗 listing_id non présent dans listings : {unknown}")

def validate_neighbourhoods(df):
    report("NEIGHBOURHOODS")
    dup = df["neighbourhood"].duplicated().sum()
    print(f"🗝️ nom de quartier en double : {dup}")
    missing = df["neighbourhood"].isna().sum()
    print(f"⚠️ noms manquants : {missing}")

def main():
    # Charger listings pour avoir la référence d'IDs et de quartiers
    listings = pd.read_csv(DIR / "listings_clean_geo.csv")
    calendar  = pd.read_csv(DIR / "calendar_clean.csv")
    reviews   = pd.read_csv(DIR / "reviews_clean.csv")
    neighb    = pd.read_csv(DIR / "neighbourhoods_clean.csv")

    validate_listings(listings)
    validate_calendar(calendar, listings["id"])
    validate_reviews(reviews, listings["id"])
    validate_neighbourhoods(neighb)

    print("\n✅ Validation terminée")

if __name__ == "__main__":
    if not DIR.exists():
        sys.exit("❌ Dossier des fichiers clean introuvable.")
    main()