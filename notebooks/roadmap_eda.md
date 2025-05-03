# 🧭 Roadmap EDA – Airbnb Montréal

Ce document détaille chaque étape de l’analyse exploratoire, avec objectifs, livrables et références aux scripts ou notebooks.

| Ordre | Étape | Objectif | Script / Notebook | Livrable |
|-------|-------|----------|-------------------|----------|
| 1 | **Structure & Qualité** | Vérifier schéma, valeurs manquantes, doublons | `notebooks/eda_01_structure.ipynb` | Rapport .md « Data Quality » |
| 2 | **Statistiques globales** | Décrire min–max–median (`price`, `min_nights`, `reviews`) | `notebooks/eda_02_stats.ipynb` | Tableau md + histogrammes PNG |
| 3 | **Distribution des prix** | Comprendre la forme globale et par `room_type` | `eda_03_price_dist.ipynb` | Histogramme PNG + boxplot PNG |
| 4 | **Prix par quartier** | Identifier top/bottom quartiers (médiane) | `eda_04_price_neighbourhood.ipynb` | Bar‑chart top 10 PNG |
| 5 | **Taux d’occupation** | Calculer occupancy % par logement puis quartier | `eda_05_occupancy.ipynb` | CSV `occupancy_by_neigh.csv` |
| 6 | **Saisonnalité** | Détecter tendances mensuelles prix & dispo | `eda_06_seasonality.ipynb` | Courbes PNG |
| 7 | **Corrélations** | Corréler prix ↔︎ reviews, rating, min nights | `eda_07_correlations.ipynb` | Heatmap PNG + interprétation |
| 8 | **Analyse des avis** | Sentiment + mots clés récurrents | `eda_08_reviews_sentiment.ipynb` | Word cloud + tableau sentiment |
| 9 | **Cartographie** | Carte choroplèthe prix médian / quartier | `eda_09_map.ipynb` | `map.html` interactif |
| 10 | **Synthèse finale** | Regrouper tous les insights clés | `docs/insights_summary.md` | Document Markdown prêt Notion |

---

## Checklist de validation

- [ ] Aucun `NaN` critique après nettoyage (`validate_clean_data.py` OK)
- [ ] Histogrammes prix sans valeurs négatives ni > 10 000 $
- [ ] `%` d’occupation compris entre 0 et 100
- [ ] Corrélations interprétées (expliquer si faibles)
- [ ] Carte affiche 100 % des quartiers (matching GeoJSON)
- [ ] Rapport final relu & copié dans Notion

---

## Conventions de nommage

- **Notebooks** : `eda_##_<topic>.ipynb`
- **Plots** : `assets/plots/<topic>_<yyyymmdd>.png`
- **Données dérivées** : `outputs/<filename>.csv` ou `.parquet`

---

## Prochaine mise à jour

Une fois l’EDA terminée, les KPI validés alimenteront :
1. **Endpoints FastAPI** (`/stats/price-median`, `/stats/occupancy`, …)
2. **Composants Nuxt** (`PriceChart.vue`, `NeighbourhoodMap.vue`)

_Fichier édité : 2025‑05‑03_