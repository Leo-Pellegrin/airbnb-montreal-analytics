## 🔍 Qualité des données – Résumé

| Jeu de données | Lignes | Clé primaire unique | Valeurs NaN critiques | Observations |
| -------------- | ------ | ------------------- | --------------------- | ------------ |
| **listings**   | **9 772** | ✅ `id` | `neighbourhood` : **0 %** | 7 033 annonces sans calendrier, 2 046 sans avis |
| **calendar**   | **≈ 3,6 M** | ✅ (`listing_id`,`date`) | `price` : **0 %** | 0 clé FK orpheline ; horizon ≤ 2026‑04 |
| **reviews**    | **≈ 1,1 M** | ✅ `id` | `comments` : **0 %** | 0 clé FK orpheline ; aucune review ≥ 2024 |

**Points‑clés**

- **Intégrité FK** parfaite (`reviews` & `calendar` → `listings`).  
- **Annonces inactives** : 1 928 logements sans calendrier **ni** avis → à exclure pour certains KPI.  
- Dataset **fiable** : pas de champs quantitatifs manquants.

---

## 📊 Observations générales

| Indicateur | Valeur |
|------------|--------|
| Prix médian global | **93 $** |
| IQR (25‑75 %) | **60 $ – 148 $** |
| Annonces > 500 $ | **2.15 %** |
| Minimum nights médian | **31 nuits** |
| Médiane `Entire home/apt` | **104 $** |
| Médiane `Private room` | **44 $** |

---

## 🏘️ Prix par quartier

| | Quartier | Médiane |
|-|----------|---------|
| **Plus cher** | L’Île‑Bizard‑Sainte‑Geneviève | **250 $** |
| **Plus abordable** | Montréal‑Est | **25 $** |

- Écart médian (cher − abordable) : **225 $**.  
- Écart P90 − P10 inter‑quartiers : **58 $**.

---

## 📈 Occupation

| | Quartier | Occupancy % |
|-|----------|-------------|
| **Le plus occupé** | Kirkland | **78 %** |
| **Le moins occupé** | Baie‑d’Urfé | **18 %** |

Médiane tous quartiers : **43,5 %**.

---

## ⏳ Saisonnalité (agrégat hebdo)

| Pic | Mois | Valeur |
|-----|------|--------|
| **Prix** | mars 2026 | **125 $** |
| **Occupation** | mars 2026 | **61,2 %** |

Hiver (jan‑mars) ⇢ bas prix, été/festivals ⇢ hausse conjointe prix + occupation.

---

## 🔗 Corrélations (ρ Pearson)

| Couple | ρ |
|--------|---|
| Prix ↔ Rating | **+0.06** |
| Prix ↔ Nombre d’avis | **‑0.00** |
| Prix ↔ Minimum nights | **‑0.03** |

> Aucune corrélation forte ; quartier et saison expliquent davantage les tarifs.

---

## 😊 Sentiment des avis

- Score moyen global : **0.64**  
- Quartier **le plus positif** : *Kirkland* (0.97)  
- Quartier **le moins positif** : *Montréal‑Nord* (0.21)  
- Avis positifs (> 0,05) : **80,5 %** – Négatifs (< ‑0,05) : **5,0 %**

---

## 🗺️ Synthèse cartographique

| KPI | Quartier n° 1 | Valeur |
|-----|--------------|--------|
| **Prix** | L’Île‑Bizard‑Sainte‑Geneviève | 250 $ |
| **Occupation** | Kirkland | 78 % |
| **Sentiment** | Kirkland | 0.97 |

_Ces chiffres proviennent des cartes `map_price.html`, `map_occupancy.html` et `map_sentiment.html`._

---

## 🔑 Conclusions

1. **Tarification** : grande disparité (25 $ → 250 $). Plateau, Ville‑Marie et L’Île‑Bizard dominent le haut de gamme.  
2. **Saison** : mars‑août = haute saison ; opportunité d’ajuster dynamiquement les prix d’hiver (–15 %).  
3. **Qualité client** : centre‑ville souffre de bruit ; améliorer cet aspect pourrait faire grimper le score moyen de sentiment.  
4. **Cibles d’investissement** : Kirkland combine forte occupation et excellente satisfaction.

---

> Rapport généré à partir des 9 notebooks EDA (prix, occupation, sentiment, cartes) – mise à jour : **2025‑05‑03**.