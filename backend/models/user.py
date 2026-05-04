"""User model — queries for the `users` table."""
from database.db import get_connection


def get_by_email(email: str):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "SELECT id, pseudo, email, password_hash, role, solde_points, statut "
        "FROM users WHERE email = ?",
        (email,),
    )
    row = cur.fetchone()
    conn.close()
    return dict(row) if row else None


def get_by_id(user_id: int):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "SELECT id, pseudo, email, role, solde_points, statut, created_at "
        "FROM users WHERE id = ?",
        (user_id,),
    )
    row = cur.fetchone()
    conn.close()
    return dict(row) if row else None


def pseudo_exists(pseudo: str) -> bool:
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT 1 FROM users WHERE pseudo = ?", (pseudo,))
    exists = cur.fetchone() is not None
    conn.close()
    return exists


def email_exists(email: str) -> bool:
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT 1 FROM users WHERE email = ?", (email,))
    exists = cur.fetchone() is not None
    conn.close()
    return exists


def create(pseudo: str, email: str, password_hash: str) -> int:
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO users (pseudo, email, password_hash) VALUES (?, ?, ?)",
        (pseudo, email, password_hash),
    )
    conn.commit()
    user_id = cur.lastrowid
    conn.close()
    return user_id


def update_profile(user_id: int, pseudo: str, email: str):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "UPDATE users SET pseudo = ?, email = ? WHERE id = ?",
        (pseudo, email, user_id),
    )
    conn.commit()
    conn.close()


def update_password(user_id: int, password_hash: str):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("UPDATE users SET password_hash = ? WHERE id = ?", (password_hash, user_id))
    conn.commit()
    conn.close()


def update_solde(user_id: int, delta: int):
    """Add delta (positive or negative) to user's points."""
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "UPDATE users SET solde_points = solde_points + ? WHERE id = ?",
        (delta, user_id),
    )
    conn.commit()
    conn.close()


def delete(user_id: int):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM users WHERE id = ?", (user_id,))
    conn.commit()
    conn.close()


def get_all(search: str = "", limit: int = 20, offset: int = 0):
    conn = get_connection()
    cur = conn.cursor()
    if search:
        cur.execute(
            "SELECT id, pseudo, email, role, solde_points, statut, created_at "
            "FROM users WHERE pseudo LIKE ? ORDER BY created_at DESC LIMIT ? OFFSET ?",
            (f"%{search}%", limit, offset),
        )
    else:
        cur.execute(
            "SELECT id, pseudo, email, role, solde_points, statut, created_at "
            "FROM users ORDER BY created_at DESC LIMIT ? OFFSET ?",
            (limit, offset),
        )
    rows = cur.fetchall()
    conn.close()
    return [dict(r) for r in rows]


def count_all(search: str = "") -> int:
    conn = get_connection()
    cur = conn.cursor()
    if search:
        cur.execute("SELECT COUNT(*) AS nb FROM users WHERE pseudo LIKE ?", (f"%{search}%",))
    else:
        cur.execute("SELECT COUNT(*) AS nb FROM users")
    row = cur.fetchone()
    conn.close()
    return dict(row)["nb"] if row else 0


def set_statut(user_id: int, statut: str):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("UPDATE users SET statut = ? WHERE id = ?", (statut, user_id))
    conn.commit()
    conn.close()


def set_role(user_id: int, role: str):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("UPDATE users SET role = ? WHERE id = ?", (role, user_id))
    conn.commit()
    conn.close()


def get_top(limit: int = 20):
    """Return top N users sorted by solde_points DESC."""
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "SELECT u.id, u.pseudo, u.solde_points, "
        "COUNT(p.id) AS nb_parties "
        "FROM users u "
        "LEFT JOIN parties p ON p.user_id = u.id "
        "GROUP BY u.id, u.pseudo, u.solde_points "
        "ORDER BY u.solde_points DESC "
        "LIMIT ?",
        (limit,),
    )
    rows = cur.fetchall()
    conn.close()
    return [dict(r) for r in rows]
