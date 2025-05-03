#!/usr/bin/env python3
"""
key_columns_finder.py
---------------------

Identifie les colonnes « clé » (unicité + non‑null) dans les datasets Airbnb
(calendar.csv(.gz), listings.csv(.gz), reviews.csv(.gz) …).

➜  python key_columns_finder.py /chemin/vers/mon/dossier
"""

import sys, gzip, pathlib, pandas as pd

# ---------- Paramètres ----------
SAMPLE_ROWS = 100_000      # nombre de lignes max à lire (pour garder le script léger)
UNIQUE_RATIO_THR = 0.999   # tolérance : ≥ 99,9 % de valeurs uniques ≈ clé candidat
# -------------------------------


def open_df(path: pathlib.Path) -> pd.DataFrame:
    """Lit un CSV ou CSV.GZ en échantillonnant éventuellement les lignes."""
    if path.suffix == ".gz":
        with gzip.open(path, "rt") as f:
            return pd.read_csv(f, nrows=SAMPLE_ROWS, low_memory=False)
    return pd.read_csv(path, nrows=SAMPLE_ROWS, low_memory=False)


def find_key_columns(df: pd.DataFrame) -> list[str]:
    """Retourne la liste des colonnes candidates à être des clés primaires/uniques."""
    candidates = []
    for col in df.columns:
        col_series = df[col]
        # Ignore les colonnes avec NaN
        if col_series.isna().any():
            continue
        # Ratio d'unicité = valeurs uniques / lignes
        unique_ratio = col_series.nunique(dropna=False) / len(col_series)
        if unique_ratio >= UNIQUE_RATIO_THR:
            candidates.append(col)
    return candidates


def main(folder: pathlib.Path):
    results = {}

    for csv_path in sorted(folder.glob("*.csv*")):
        try:
            df = open_df(csv_path)
        except Exception as e:
            print(f"⚠️  Impossible de lire {csv_path.name}: {e}")
            continue

        keys = find_key_columns(df)
        results[csv_path.name] = keys if keys else ["(aucune colonne unique)"]

    # --------- Affichage final ----------
    print("\n=== Colonnes clés candidates par fichier ===")
    for fname, cols in results.items():
        print(f"• {fname}: {', '.join(cols)}")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python key_columns_finder.py <dossier_datasets>")
        sys.exit(1)
    main(pathlib.Path(sys.argv[1]).expanduser())