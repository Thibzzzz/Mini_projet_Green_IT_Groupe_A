# GreenBet ♠ — Le casino le plus Green

Projet pédagogique EFREI Paris — Numérique Durable TI616.
Casino fictif éco-conçu : zéro argent réel, zéro framework lourd, zéro tracker.

## Lancer le projet en local

```bash
# 1. Dépendances Python
pip install -r requirements.txt

# 2a. SQLite (développement local — création automatique au 1er lancement)
python backend/app.py

# 2b. MySQL (optionnel, production)
mysql -u root -p < database/schema.sql
# puis configurer les variables d'environnement DB_ENGINE=mysql, MYSQL_*
python backend/app.py
```

Le serveur démarre sur `http://127.0.0.1:5000`.

## Minifier les assets (CSS/JS)

Le projet sert par défaut des fichiers minifiés (`static/css/style.min.css`, `static/js/*.min.js`).

```bash
python backend/minify_assets.py
```

## Compte admin par défaut

| Email | Mot de passe |
|-------|-------------|
| `admin@greenbet.fr` | `admin1234` |

> **Note** : le hash bcrypt de `admin1234` est pré-inséré dans le schéma SQL.
> Pour SQLite, le compte est créé automatiquement via `init_sqlite()`.

## Structure

```
GreenBet/
├── frontend/
│   ├── templates/       # Jinja2 HTML
│   └── static/          # CSS + JS vanilla
├── backend/
│   ├── app.py           # Entrée Flask
│   ├── config.py        # Config DB / sessions
│   ├── controllers/     # Blueprints Flask (MVC)
│   ├── models/          # Couche accès données
│   └── database/        # Schema + SQLite DB
├── requirements.txt
├── .env.example
└── GREEN.md
```

## Jeux disponibles

| Jeu | Description |
|-----|-------------|
| ♠ Blackjack | JS vanilla, 52 cartes, Fisher-Yates, résultat sauvé côté serveur |
| ⚫ Roulette verte | Résultat généré **côté serveur** uniquement (anti-triche) |
| ♦ Bataille du croupier | Une carte vs une carte, le plus haut gagne (JS vanilla) |

## Engagements Green IT

→ Voir `GREEN.md`

## Déploiement (général)

- Configurer `SECRET_KEY` en variable d’environnement.
- Choisir la base:
  - `DB_ENGINE=sqlite` (démo / local)
  - ou `DB_ENGINE=mysql` + `MYSQL_HOST`, `MYSQL_USER`, `MYSQL_PASSWORD`, `MYSQL_DATABASE` (production)
- Sessions: optionnel `SESSION_FILE_DIR` (ex: `/tmp/greenbet_sessions`).

### Notes importantes

- Ne jamais versionner `.env` (voir `.gitignore`).
- Le fichier `.env.example` documente les variables attendues.
- SQLite est pratique mais pas idéal pour de la persistance en prod.
