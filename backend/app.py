"""GreenBet — point d'entrée Flask."""
import os
import secrets
import tempfile
from pathlib import Path
from flask import Flask, render_template, session
from flask_session import Session

import config
from database.db import init_sqlite
from controllers.auth import auth_bp
from controllers.user import user_bp
from controllers.jeu import jeu_bp
from controllers.partie import partie_bp
from controllers.admin import admin_bp

HERE = Path(__file__).resolve().parent
FRONTEND = HERE.parent / "frontend"
app = Flask(
    __name__,
    template_folder=str(FRONTEND / "templates"),
    static_folder=str(FRONTEND / "static"),
)
app.secret_key = config.SECRET_KEY
app.config["SESSION_TYPE"] = config.SESSION_TYPE
app.config["SESSION_PERMANENT"] = config.SESSION_PERMANENT
session_dir = os.environ.get("SESSION_FILE_DIR")
if not session_dir:
    session_dir = os.path.join(tempfile.gettempdir(), "greenbet_sessions")
os.makedirs(session_dir, exist_ok=True)
app.config["SESSION_FILE_DIR"] = session_dir

Session(app)

app.register_blueprint(auth_bp)
app.register_blueprint(user_bp)
app.register_blueprint(jeu_bp)
app.register_blueprint(partie_bp)
app.register_blueprint(admin_bp)

@app.before_request
def ensure_csrf():
    if "_csrf_token" not in session:
        session["_csrf_token"] = secrets.token_hex(16)

@app.context_processor
def inject_csrf():
    return {"csrf_token": session.get("_csrf_token", "")}


from flask import Blueprint
main_bp = Blueprint("main", __name__)

@main_bp.route("/")
def index():
    return render_template("index.html")

app.register_blueprint(main_bp)


@app.errorhandler(404)
def not_found(e):
    return render_template("errors/404.html"), 404

@app.errorhandler(403)
def forbidden(e):
    return render_template("errors/403.html"), 403


if config.DB_ENGINE == "sqlite":
    os.makedirs(os.path.dirname(config.SQLITE_PATH), exist_ok=True)
    if not os.path.exists(config.SQLITE_PATH):
        init_sqlite()


if __name__ == "__main__":
    app.run(debug=os.environ.get("FLASK_DEBUG", "1") == "1")
