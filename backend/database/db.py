"""
Database helper — supports SQLite (dev) and MySQL (prod).
All queries use parameterised statements to prevent SQL injection.
"""
import sqlite3
import os
import config


def get_connection():
    """Return a DB connection depending on DB_ENGINE config."""
    if config.DB_ENGINE == "mysql":
        import mysql.connector
        return mysql.connector.connect(
            host=config.MYSQL_HOST,
            user=config.MYSQL_USER,
            password=config.MYSQL_PASSWORD,
            database=config.MYSQL_DATABASE,
        )
    else:
        conn = sqlite3.connect(config.SQLITE_PATH)
        conn.row_factory = sqlite3.Row
        conn.execute("PRAGMA foreign_keys = ON")
        return conn


def init_sqlite():
    """Initialise the SQLite database from schema.sql (dev only)."""
    schema_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "schema.sql")
    with open(schema_path, encoding="utf-8") as f:
        raw = f.read()

    lines = []
    for line in raw.splitlines():
        stripped = line.strip()
        if stripped.startswith("--") or not stripped:
            continue
        lines.append(line)
    raw = "\n".join(lines)

    raw = raw.replace("INT PRIMARY KEY AUTO_INCREMENT", "INTEGER PRIMARY KEY AUTOINCREMENT")
    raw = raw.replace("AUTO_INCREMENT", "")
    raw = raw.replace("ENUM('joueur', 'admin')", "TEXT CHECK(role IN ('joueur','admin'))")
    raw = raw.replace("ENUM('actif', 'banni')", "TEXT CHECK(statut IN ('actif','banni'))")
    raw = raw.replace("ENUM('gagne', 'perdu', 'nul')", "TEXT CHECK(resultat IN ('gagne','perdu','nul'))")
    raw = raw.replace("BOOLEAN", "INTEGER")
    raw = raw.replace("TRUE", "1")
    raw = raw.replace("FALSE", "0")

    statements = [s.strip() for s in raw.split(";") if s.strip()]

    conn = get_connection()
    cur = conn.cursor()
    for stmt in statements:
        try:
            cur.execute(stmt)
        except Exception:
            pass
    conn.commit()
    conn.close()
