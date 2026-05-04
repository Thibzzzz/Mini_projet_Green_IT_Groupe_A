import os
import secrets

SECRET_KEY = os.environ.get("SECRET_KEY", secrets.token_hex(32))

# --- Database ---
DB_ENGINE = os.environ.get("DB_ENGINE", "sqlite")

SQLITE_PATH = os.path.join(os.path.dirname(__file__), "database", "greenbet.db")

MYSQL_HOST     = os.environ.get("MYSQL_HOST", "localhost")
MYSQL_USER     = os.environ.get("MYSQL_USER", "root")
MYSQL_PASSWORD = os.environ.get("MYSQL_PASSWORD", "")
MYSQL_DATABASE = os.environ.get("MYSQL_DATABASE", "greenbet")

# --- Session ---
SESSION_TYPE = "filesystem"
SESSION_PERMANENT = False
