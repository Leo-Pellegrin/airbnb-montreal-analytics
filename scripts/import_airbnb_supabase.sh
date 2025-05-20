#!/usr/bin/env bash
# ===============================================================
#  import_airbnb_supabase.sh
#  -------------------------
#  Initialise le schéma Airbnb Montréal
#  + importe les CSV propres dans Supabase via psql \copy.
#
#  Usage :
#     PGURL="postgresql://postgres:<PW>@...:5432/postgres?sslmode=require" \
#     ./scripts/import_airbnb_supabase.sh
#
#  (PGURL = chaîne Postgres pooler depuis Supabase Settings)
# ===============================================================

set -euo pipefail

PGURL="${PGURL:-}"
CLEAN_DIR="./clean"   # dossier contenant listings_clean_geo.csv, etc.

if [[ -z "$PGURL" ]]; then
  echo "❌  Variable PGURL non définie."
  exit 1
fi

echo "🔗  Connexion  : $PGURL"
echo "📂  Source CSV : $CLEAN_DIR"
echo "--------------------------------------------------------"

# ---------- 1. Suppression des tables existantes --------------------
echo "🗑️  Suppression des tables existantes..."
psql "$PGURL" <<'SQL'
DROP TABLE IF EXISTS public.calendar_weekly CASCADE;
DROP TABLE IF EXISTS public.reviews CASCADE;
DROP TABLE IF EXISTS public.listings CASCADE;
DROP TABLE IF EXISTS public.neighbourhoods CASCADE;
SQL

# ---------- 2. Schéma (tables, index, RLS) --------------------
psql "$PGURL" <<'SQL'
BEGIN;

-- Suppression des tables existantes
DROP TABLE IF EXISTS public.neighbourhoods;
DROP TABLE IF EXISTS public.listings;
DROP TABLE IF EXISTS public.calendar_weekly;
DROP TABLE IF EXISTS public.reviews;

-- neighbourhoods
CREATE TABLE IF NOT EXISTS public.neighbourhoods (
  neighbourhood text PRIMARY KEY
);

-- listings
CREATE TABLE IF NOT EXISTS public.listings (
  id bigint PRIMARY KEY,
  host_id bigint NOT NULL,
  name text NOT NULL,
  description text,
  neighbourhood text REFERENCES public.neighbourhoods(neighbourhood),
  latitude double precision NOT NULL,
  longitude double precision NOT NULL,
  room_type text NOT NULL,
  price numeric(10,2) NOT NULL,
  minimum_nights integer NOT NULL,
  number_of_reviews integer NOT NULL,
  last_review date,
  review_scores_rating numeric(5,2),
  amenities text
);

-- calendar_weekly: agrégat hebdomadaire pour éviter le trop-plein de lignes
CREATE TABLE IF NOT EXISTS public.calendar_weekly (
  listing_id bigint REFERENCES public.listings(id) ON DELETE CASCADE,
  week_id   date    NOT NULL,
  avg_price     numeric(10,2) NOT NULL,
  occupancy_pct numeric(5,4) NOT NULL,
  PRIMARY KEY (listing_id, week_id)
);

-- reviews
CREATE TABLE IF NOT EXISTS public.reviews (
  id bigint PRIMARY KEY,
  listing_id bigint REFERENCES public.listings(id) ON DELETE CASCADE,
  date date NOT NULL,
  reviewer_id bigint,
  reviewer_name text,
  comments text NOT NULL
);

-- Indexes
CREATE INDEX IF NOT EXISTS idx_listings_neigh           ON public.listings        (neighbourhood);
CREATE INDEX IF NOT EXISTS idx_calendar_weekly_listing   ON public.calendar_weekly (listing_id);
CREATE INDEX IF NOT EXISTS idx_calendar_weekly_week      ON public.calendar_weekly (week_id);
CREATE INDEX IF NOT EXISTS idx_reviews_listing_date      ON public.reviews         (listing_id, date);

COMMIT;
SQL

# ---------- 3. Vider tables (ordre enfants -> parents) --------
psql "$PGURL" -c "TRUNCATE TABLE public.calendar_weekly CASCADE;"
psql "$PGURL" -c "TRUNCATE TABLE public.reviews         CASCADE;"
psql "$PGURL" -c "TRUNCATE TABLE public.listings        CASCADE;"
psql "$PGURL" -c "TRUNCATE TABLE public.neighbourhoods  CASCADE;"

# ---------- 4. Import CSV via \copy ---------------------------
echo "⬆️  Import CSV ..."

psql "$PGURL" <<SQL
\copy public.neighbourhoods (neighbourhood) FROM '$CLEAN_DIR/neighbourhoods_clean.csv' CSV HEADER;
\copy public.listings (id, host_id, name, description, neighbourhood, latitude, longitude, room_type, price, minimum_nights, number_of_reviews, last_review, review_scores_rating, amenities) FROM '$CLEAN_DIR/listings_clean_geo.csv' CSV HEADER DELIMITER ',' QUOTE '"';
\copy public.calendar_weekly FROM '$CLEAN_DIR/calendar_weekly_clean.csv' CSV HEADER;
\copy public.reviews FROM '$CLEAN_DIR/reviews_clean.csv' CSV HEADER;
SQL

# ---------- 5. Récap lignes -----------------------------------
echo "✅  Import terminé. Compte des lignes :"
psql "$PGURL" -c "
SELECT 'neighbourhoods' AS table_name, COUNT(*) FROM public.neighbourhoods UNION ALL
SELECT 'listings'       AS table_name, COUNT(*) FROM public.listings       UNION ALL
SELECT 'calendar_weekly'AS table_name, COUNT(*) FROM public.calendar_weekly UNION ALL
SELECT 'reviews'        AS table_name, COUNT(*) FROM public.reviews;
"