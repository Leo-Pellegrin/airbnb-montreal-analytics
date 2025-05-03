# 🏡 Montréal Airbnb Analytics Dashboard

**Analyse de données + Dashboard full‑stack**  
Données brutes → ETL Python → PostgreSQL (Supabase) → API FastAPI → Front Nuxt 3

---

## 📑 Sommaire
1. [Prérequis](#prérequis)
2. [Structure du dépôt](#structure-du-dépôt)
3. [Pipeline ETL](#pipeline-etl)
4. [Analyse exploratoire (EDA)](#analyse-exploratoire-eda)
5. [Stack technique](#stack-technique)
6. [Lancement rapide](#lancement-rapide)
7. [Road Map](#road-map)
8. [Licence](#licence)

---

## Prérequis
- **Python 3.10+** (`pipx` conseillé)
- **Node 18+** (Nuxt 3, pnpm)
- **Supabase CLI** (`npm i -g supabase`)
- `psql` (ou Docker + pgcli)
- Comptes : Supabase, Vercel

## Structure du dépôt

├─ clean/                   # CSV nettoyés prêts à l’import
├─ notebooks/               # EDA Jupyter
├─ scripts/
│   ├─ key_columns_finder.py     # détection colonnes clé (PK) dans CSV bruts
│   ├─ clean_data.py             # pipeline de nettoyage initial
│   ├─ assign_neighbourhoods.py  # jointure spatiale → quartier
│   ├─ validate_clean_data.py    # contrôles qualité avant import
│   └─ import_airbnb_supabase.sh # import CSV → Supabase (optionnel
├─ backend/                 # FastAPI (src/)
├─ frontend/                # Nuxt 3 (app/)
└─ README.md

## Pipeline ETL & Qualité

| Étape | Script / commande | Résultat |
|-------|-------------------|----------|
| 1 | `python scripts/key_columns_finder.py ./raw_data` | Vérifie unicité & clés candidates |
| 2 | `python scripts/clean_data.py` | Génère `clean/*_clean.csv` |
| 3 | `python scripts/assign_neighbourhoods.py` | Ajoute `neighbourhood` manquants → `listings_clean_geo.csv` |
| 4 | `python scripts/validate_clean_data.py ./clean` | Contrôle intégrité / valeur manquante **0** |
| 5 | `PGURL=... ./scripts/import_airbnb_supabase.sh` *(ou `\COPY` via psql)* | Charge les données dans Supabase |

> Après l’étape 4, la sortie doit afficher `neighbourhood : 0` et `id en double : 0`.  
> L’import (étape 5) est optionnel, on peut utiliser `COPY FROM 'supabase://...'` dans le SQL Editor.

## Analyse exploratoire (EDA)
Les notebooks `notebooks/eda_*.ipynb` couvrent :
- Structure & qualité
- Distribution des prix
- Prix par quartier
- Saisonnalité, corrélations, sentiment des avis
- Carte choroplèthe quartiers

## Stack technique
| Couche | Techno |
|--------|--------|
| Base de données | **PostgreSQL 15** (Supabase pooler) |
| Backend | **FastAPI** + asyncpg |
| Frontend | **Nuxt 3** + Vue 3 + Chart.js |
| Auth | Supabase Auth (JWT) |
| Déploiement | Vercel (front) / Render ou Railway (API) |

## Lancement rapide
```bash
# 1. Cloner le repo & installer Python env
git clone https://github.com/Leo-Pellegrin/airbnb-montreal-analytics.git
cd airbnb-montreal-analytics
pipx runpip python -e . '[dev]'

# 2. Nettoyage + ajout quartiers + validation
python scripts/key_columns_finder.py ./raw_data
python scripts/clean_data.py
python scripts/assign_neighbourhoods.py
python scripts/validate_clean_data.py ./clean

# 3. Import (Supabase)
PGURL="postgresql://user:pw@host:6543/postgres?sslmode=require" \
./scripts/import_airbnb_supabase.sh

# 3. Frontend
cd frontend && pnpm i && pnpm dev

# 4. Backend
cd backend && uvicorn app.main:app --reload
```

## Road Map

La feuille de route détaillée se trouve dans notebooks/roadmap_eda.md.

## Licence

MIT © 2025 Léo Pellegrin