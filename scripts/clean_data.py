import pandas as pd
from pathlib import Path
from datetime import datetime

DATA_DIR = Path("./dataset")          # dossier où sont les .gz/.csv
OUT_DIR  = Path("./clean")     # dossier de sortie
OUT_DIR.mkdir(exist_ok=True)

def clean_price(series: pd.Series) -> pd.Series:
    """
    Nettoie une série de prix :
      • enlève tout caractère non numérique ou point
      • convertit en float (NaN si conversion impossible)
    """
    cleaned = (
        series.astype(str)
              .str.strip()                      
              .str.replace(r"[^\d\.]", "", regex=True)
    )
    # Pandas convertit → float, 'errors=\"coerce\"' force les valeurs impossibles à NaN
    return pd.to_numeric(cleaned, errors="coerce")

def tidy_listings():
    df = pd.read_csv(DATA_DIR/"listings.csv.gz", low_memory=False)

    keep_cols = [
        "id","host_id","name","description","neighbourhood",
        "latitude","longitude","room_type","price",
        "minimum_nights","number_of_reviews",
        "last_review","review_scores_rating","amenities"
    ]
    df = df[keep_cols]

    df["price"] = clean_price(df["price"]).fillna(0)   
    df["last_review"]  = pd.to_datetime(df["last_review"], errors="coerce")
    df["amenities"]    = (
        df["amenities"]
        .str.strip("{}")
        .str.replace('"', "")
        .fillna("")
    )

    df = df.drop_duplicates(subset="id")
    df.to_csv(OUT_DIR/"listings_clean.csv", index=False)

def tidy_calendar():
    df = pd.read_csv(DATA_DIR/"calendar.csv.gz", low_memory=False)
    df = df[["listing_id","date","available","price","minimum_nights"]]

    df["date"]      = pd.to_datetime(df["date"])
    df["price"]     = clean_price(df["price"]).fillna(0)
    df["available"] = df["available"].map({"t": True, "f": False})

    df.to_csv(OUT_DIR/"calendar_clean.csv", index=False)

def tidy_reviews():
    df = pd.read_csv(DATA_DIR/"reviews.csv.gz", low_memory=False)
    df = df[["id","listing_id","date","reviewer_id","reviewer_name","comments"]]

    df["date"] = pd.to_datetime(df["date"])
    df = df.dropna(subset=["comments","listing_id"])
    df = df.drop_duplicates(subset="id")

    df.to_csv(OUT_DIR/"reviews_clean.csv", index=False)

def tidy_neighbourhoods():
    df = pd.read_csv(DATA_DIR/"neighbourhoods.csv")
    df["neighbourhood"] = df["neighbourhood"].str.strip()
    df.to_csv(OUT_DIR/"neighbourhoods_clean.csv", index=False)

if __name__ == "__main__":
    tidy_listings()
    tidy_calendar()
    tidy_reviews()
    tidy_neighbourhoods()
    print("✅ Fichiers nettoyés dans ./clean/")