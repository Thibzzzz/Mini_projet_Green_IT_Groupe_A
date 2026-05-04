"""Partie model — queries for the `parties` table."""
from database.db import get_connection


def save(user_id: int, jeu_id: int, resultat: str, points_gagnes: int) -> int:
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO parties (user_id, jeu_id, resultat, points_gagnes) "
        "VALUES (?, ?, ?, ?)",
        (user_id, jeu_id, resultat, points_gagnes),
    )
    conn.commit()
    partie_id = cur.lastrowid
    conn.close()
    return partie_id


def get_last_by_user(user_id: int, limit: int = 5):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "SELECT p.id, j.nom AS jeu, p.resultat, p.points_gagnes, p.joue_le "
        "FROM parties p "
        "JOIN jeux j ON j.id = p.jeu_id "
        "WHERE p.user_id = ? "
        "ORDER BY p.joue_le DESC "
        "LIMIT ?",
        (user_id, limit),
    )
    rows = cur.fetchall()
    conn.close()
    return [dict(r) for r in rows]


def count_by_user(user_id: int) -> int:
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT COUNT(*) AS nb FROM parties WHERE user_id = ?", (user_id,))
    row = cur.fetchone()
    conn.close()
    return dict(row)["nb"] if row else 0


def classement(limit: int = 20):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "SELECT u.pseudo, u.solde_points, COUNT(p.id) AS nb_parties "
        "FROM users u "
        "LEFT JOIN parties p ON p.user_id = u.id "
        "WHERE u.statut = 'actif' "
        "GROUP BY u.id, u.pseudo, u.solde_points "
        "ORDER BY u.solde_points DESC "
        "LIMIT ?",
        (limit,),
    )
    rows = cur.fetchall()
    conn.close()
    return [dict(r) for r in rows]
