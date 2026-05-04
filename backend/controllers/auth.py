"""Auth controller — inscription, connexion, déconnexion."""
import bcrypt
from flask import Blueprint, render_template, request, redirect, url_for, session, flash
import models.user as UserModel

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        pseudo = request.form.get("pseudo", "").strip()
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")
        confirm = request.form.get("confirm", "")

        errors = []
        if not pseudo or len(pseudo) < 3:
            errors.append("Le pseudo doit faire au moins 3 caractères.")
        if not email or "@" not in email:
            errors.append("Adresse email invalide.")
        if len(password) < 8:
            errors.append("Le mot de passe doit faire au moins 8 caractères.")
        if password != confirm:
            errors.append("Les mots de passe ne correspondent pas.")
        if UserModel.pseudo_exists(pseudo):
            errors.append("Ce pseudo est déjà pris.")
        if UserModel.email_exists(email):
            errors.append("Cet email est déjà utilisé.")

        if errors:
            return render_template("auth/register.html", errors=errors, pseudo=pseudo, email=email)

        hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
        user_id = UserModel.create(pseudo, email, hashed)
        session["user_id"] = user_id
        session["pseudo"] = pseudo
        session["role"] = "joueur"
        flash("Bienvenue sur GreenBet ! Votre compte a été créé.", "success")
        return redirect(url_for("user.dashboard"))

    return render_template("auth/register.html", errors=[], pseudo="", email="")


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")

        user = UserModel.get_by_email(email)
        if not user:
            return render_template("auth/login.html", error="Identifiants incorrects.")
        if user["statut"] == "banni":
            return render_template("auth/login.html", error="Votre compte a été suspendu.")
        if not bcrypt.checkpw(password.encode(), user["password_hash"].encode()):
            return render_template("auth/login.html", error="Identifiants incorrects.")

        session["user_id"] = user["id"]
        session["pseudo"] = user["pseudo"]
        session["role"] = user["role"]
        flash(f"Bienvenue, {user['pseudo']} !", "success")
        return redirect(url_for("user.dashboard"))

    return render_template("auth/login.html", error=None)


@auth_bp.route("/logout")
def logout():
    session.clear()
    flash("Vous avez été déconnecté.", "info")
    return redirect(url_for("main.index"))
