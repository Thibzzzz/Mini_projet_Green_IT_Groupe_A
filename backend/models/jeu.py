"""Jeux model — queries for the `jeux` table."""
from functools import lru_cache
from database.db import get_connection


def get_all_actifs():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT id, nom, description FROM jeux WHERE actif = 1")
    rows = cur.fetchall()
    conn.close()
    return [dict(r) for r in rows]


def get_main_games(limit: int = 3):
    """
    Return unique active games for the catalogue home section.
    Deduplicates by game name and keeps only the first entries.
    """
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        """
        SELECT MIN(id) AS id, nom, MIN(description) AS description
        FROM jeux
        WHERE actif = 1
        GROUP BY nom
        ORDER BY id
        LIMIT ?
        """,
        (limit,),
    )
    rows = cur.fetchall()
    conn.close()
    return [dict(r) for r in rows]


@lru_cache(maxsize=1)
def get_main_games_cached():
    """Simple cache for catalogue cards."""
    return tuple((g["id"], g["nom"], g["description"]) for g in get_main_games(3))


def clear_catalog_cache():
    get_main_games_cached.cache_clear()


def get_by_id(jeu_id: int):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "SELECT id, nom, description, min_joueurs, max_joueurs, actif "
        "FROM jeux WHERE id = ?",
        (jeu_id,),
    )
    row = cur.fetchone()
    conn.close()
    return dict(row) if row else None


def get_all_paginated(search: str = "", limit: int = 20, offset: int = 0):
    conn = get_connection()
    cur = conn.cursor()
    if search:
        cur.execute(
            "SELECT id, nom, description, min_joueurs, max_joueurs, actif "
            "FROM jeux WHERE nom LIKE ? "
            "ORDER BY id ASC LIMIT ? OFFSET ?",
            (f"%{search}%", limit, offset),
        )
    else:
        cur.execute(
            "SELECT id, nom, description, min_joueurs, max_joueurs, actif "
            "FROM jeux ORDER BY id ASC LIMIT ? OFFSET ?",
            (limit, offset),
        )
    rows = cur.fetchall()
    conn.close()
    return [dict(r) for r in rows]


def count_all(search: str = "") -> int:
    conn = get_connection()
    cur = conn.cursor()
    if search:
        cur.execute("SELECT COUNT(*) AS nb FROM jeux WHERE nom LIKE ?", (f"%{search}%",))
    else:
        cur.execute("SELECT COUNT(*) AS nb FROM jeux")
    row = cur.fetchone()
    conn.close()
    return dict(row)["nb"] if row else 0


def create(nom: str, description: str, min_joueurs: int, max_joueurs: int, actif: int) -> int:
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO jeux (nom, description, min_joueurs, max_joueurs, actif) "
        "VALUES (?, ?, ?, ?, ?)",
        (nom, description, min_joueurs, max_joueurs, actif),
    )
    conn.commit()
    jeu_id = cur.lastrowid
    conn.close()
    clear_catalog_cache()
    return jeu_id


def update(jeu_id: int, nom: str, description: str, min_joueurs: int, max_joueurs: int, actif: int):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "UPDATE jeux SET nom = ?, description = ?, min_joueurs = ?, max_joueurs = ?, actif = ? "
        "WHERE id = ?",
        (nom, description, min_joueurs, max_joueurs, actif, jeu_id),
    )
    conn.commit()
    conn.close()
    clear_catalog_cache()


def delete(jeu_id: int):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM jeux WHERE id = ?", (jeu_id,))
    conn.commit()
    conn.close()
    clear_catalog_cache()
