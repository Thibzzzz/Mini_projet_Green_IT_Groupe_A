# GreenBet — Choix Green IT & Numérique Durable

Projet EFREI Paris — TI616 Numérique Durable

---

## 1. Zéro framework CSS (Bootstrap, Tailwind…)

**Choix** : CSS vanilla avec variables CSS (`:root`).

**Impact estimé** :
- Bootstrap 5 minifié : **~160 Ko** (CSS) + ~39 Ko (JS)
- GreenBet `style.css` : **< 8 Ko**
- **Économie : ~192 Ko par page** soit −96 % de poids CSS/JS framework

**Bénéfice Green IT** : moins de données transférées → moins d'énergie réseau, moins de CPU pour parser.

---

## 2. Zéro framework JavaScript (React, Vue, Angular)

**Choix** : JS vanilla ES6+ uniquement, deux fichiers < 5 Ko chacun.

**Impact estimé** :
- React 18 + ReactDOM (prod min) : **~130 Ko**
- Vue 3 (prod min) : **~100 Ko**
- GreenBet JS total : **< 10 Ko**
- **Économie : ~120–130 Ko** par page

**Bénéfice Green IT** : parsing JS moins coûteux, exécution plus rapide, moins de CO₂ pour le processeur client.

---

## 3. Polices système uniquement

**Choix** : `font-family: system-ui, -apple-system, sans-serif;`

**Impact estimé** :
- Chargement Google Fonts (2 weights) : **~30–80 Ko** + 1–2 requêtes DNS+TCP supplémentaires
- GreenBet : **0 requête externe**, 0 Ko téléchargé
- **Économie : ~50 Ko + 2 round-trips réseau** → réduction de latence dès le premier chargement

**Bénéfice Green IT** : zéro donnée transmise à des tiers, meilleure vie privée, chargement instantané.

---

## 4. Zéro tracker tiers

**Choix** : aucun Google Analytics, aucun pixel publicitaire, aucun script tiers.

**Impact estimé** :
- Google Analytics 4 : **~17 Ko** de JS + 1 requête vers `google-analytics.com` à chaque chargement
- Facebook Pixel : **~50 Ko** + requête vers `facebook.net`
- **Économie : ~70 Ko + 2 requêtes tiers** à chaque visite

**Bénéfice Green IT** : aucune donnée collectée inutilement, protection du RGPD, réduction de la consommation réseau, suppression de dépendances critiques de disponibilité.

---

## 5. Pages générées côté serveur (SSR Flask)

**Choix** : architecture MVC, pages HTML complètes envoyées par Flask/Jinja2.

**Impact estimé** :
- Avec une SPA React : bundle JS initial **> 200 Ko**, premier rendu retardé (hydratation)
- Avec Flask SSR : HTML complet envoyé d'emblée, **0 étape d'hydratation**
- Page d'accueil GreenBet estimée : **< 20 Ko** total (HTML + CSS inline)

**Bénéfice Green IT** : TTI (Time to Interactive) minimal, moins de CPU côté client, compatible avec les connexions lentes.

---

## 6. Icônes Unicode natifs

**Choix** : symboles Unicode ♠ ♥ ♦ ♣ ✓ → directement dans le HTML.

**Impact estimé** :
- Font Awesome CDN : **~160 Ko** (fonts + CSS)
- MaterialSymbols : **~130 Ko**
- GreenBet : **0 Ko** d'icônes

**Bénéfice Green IT** : aucun fichier de police d'icônes, aucune requête externe.

---

## 7. Objectifs de poids des pages

| Page | Objectif | Estimation atteinte |
|------|----------|---------------------|
| Accueil (`/`) | < 20 Ko | ~18 Ko |
| Dashboard (`/dashboard`) | < 30 Ko | ~22 Ko |
| Blackjack (`/jeux/blackjack`) | < 35 Ko | ~28 Ko |
| Roulette (`/jeux/roulette`) | < 30 Ko | ~22 Ko |
| Admin (`/admin/users`) | < 40 Ko | ~30 Ko |

> Les tailles estimées incluent HTML + CSS + JS (sans images car zéro image raster).

---

## 8. Évolutions possibles (hors MVP)

- Activation d'un en-tête HTTP `Cache-Control` pour mettre le CSS en cache navigateur
- Compression gzip/brotli des réponses Flask (`flask-compress`)
- Hébergement sur PythonAnywhere ou Render en région européenne (→ mix électrique plus green)
- Dark mode système via `@media (prefers-color-scheme: dark)` (sans JS)

---

## Bilan Green IT global

> En remplaçant Bootstrap + React + Google Fonts + Google Analytics par des équivalents natifs ou systèmes,
> GreenBet économise **environ 500 Ko** de données transférées par visite, soit une réduction estimée de **−42 %** 
> de l'empreinte carbone numérique par rapport à un site casino classique avec stack React/Bootstrap.

*Calcul indicatif basé sur le CO₂ émis par Ko transféré (source : Website Carbon Calculator, 2024).*
