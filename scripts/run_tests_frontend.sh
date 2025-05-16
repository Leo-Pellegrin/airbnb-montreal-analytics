#!/usr/bin/env bash
set -euo pipefail

FRONTEND_DIR="$(dirname "$0")/.."/frontend

echo "🔬 Lancement des tests unitaires et snapshots (Vitest)"
cd "$FRONTEND_DIR"
npx vitest run

echo "🔍 Lancement des tests d'accessibilité (Vitest + axe)"
npx vitest run tests/a11y

if [ -d "cypress" ]; then
  echo "🚦 Lancement des tests end-to-end (Cypress)"
  npx cypress run
fi

echo
echo "✅ Tous les tests frontend sont passés avec succès !"
