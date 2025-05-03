#!/usr/bin/env bash
# ===============================================================
#  import_airbnb_supabase.sh
#  -------------------------
#  Initialise le schéma Airbnb Montréal
#  + importe les CSV propres dans Supabase via psql \copy.
#
#  Usage :
#     PGURL="postgresql://postgres:<PW>@aws-0-us-east-2.pooler.supabase.com:6543/postgres?sslmode=require" \
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

# ---------- 1. Schéma (tables, index, RLS) --------------------
psql "$PGURL" <<'SQL'
BEGIN;

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
  amenities text,
  created_at timestamptz DEFAULT now()
);

-- calendar
CREATE TABLE IF NOT EXISTS public.calendar (
  listing_id bigint REFERENCES public.listings(id) ON DELETE CASCADE,
  date date NOT NULL,
  available boolean NOT NULL,
  price numeric(10,2) NOT NULL,
  minimum_nights integer NOT NULL,
  PRIMARY KEY (listing_id, date)
);

-- reviews
CREATE TABLE IF NOT EXISTS public.reviews (
  id bigint PRIMARY KEY,
  listing_id bigint REFERENCES public.listings(id) ON DELETE CASCADE,
  date date NOT NULL,
  reviewer_id bigint,
  reviewer_name text,
  comments text NOT NULL,
  created_at timestamptz DEFAULT now()
);

-- Indexes
CREATE INDEX IF NOT EXISTS idx_listings_neigh   ON public.listings  (neighbourhood);
CREATE INDEX IF NOT EXISTS idx_calendar_date    ON public.calendar  (date);
CREATE INDEX IF NOT EXISTS idx_reviews_listing_date ON public.reviews (listing_id, date);

COMMIT;
SQL

# ---------- 2. Vider tables (ordre enfants -> parents) --------
psql "$PGURL" -c "TRUNCATE TABLE public.calendar    CASCADE;"
psql "$PGURL" -c "TRUNCATE TABLE public.reviews     CASCADE;"
psql "$PGURL" -c "TRUNCATE TABLE public.listings    CASCADE;"
psql "$PGURL" -c "TRUNCATE TABLE public.neighbourhoods CASCADE;"

# ---------- 3. Import CSV via \copy ---------------------------
echo "⬆️  Import CSV ..."

psql "$PGURL" <<SQL
\copy public.neighbourhoods (neighbourhood)    FROM '$CLEAN_DIR/neighbourhoods_clean.csv'    CSV HEADER;
\copy public.listings                          FROM '$CLEAN_DIR/listings_clean_geo.csv'      CSV HEADER;
\copy public.calendar                          FROM '$CLEAN_DIR/calendar_clean.csv'          CSV HEADER;
\copy public.reviews                           FROM '$CLEAN_DIR/reviews_clean.csv'           CSV HEADER;
SQL

# ---------- 4. Récap lignes -----------------------------------
echo "✅  Import terminé. Compte des lignes :"
psql "$PGURL" -c "
SELECT 'listings' AS table, COUNT(*) FROM public.listings UNION ALL
SELECT 'calendar', COUNT(*) FROM public.calendar UNION ALL
SELECT 'reviews', COUNT(*) FROM public.reviews UNION ALL
SELECT 'neighbourhoods', COUNT(*) FROM public.neighbourhoods;
"