#!/usr/bin/env bash
set -euo pipefail

# Chemin vers le dossier backend (ajuste si besoin)
BACKEND_DIR="$(dirname "$0")/.."/backend

echo "🔬 Lancement des tests backend (pytest)"
cd "$BACKEND_DIR"
source .venv/bin/activate
PYTHONPATH=. pytest --maxfail=1 --disable-warnings -q

echo "🔍 Lancement du linting (black)"
black .
echo "🔍 Lancement du linting (flake8)"
flake8 .

echo
echo "✅ Tous les tests et le linting sont passés avec succès !"