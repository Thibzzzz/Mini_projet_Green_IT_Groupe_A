"""User controller — dashboard, profil, suppression compte."""
import bcrypt
from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from functools import wraps
import models.user as UserModel
import models.partie as PartieModel

user_bp = Blueprint("user", __name__)


def login_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if "user_id" not in session:
            flash("Vous devez être connecté pour accéder à cette page.", "error")
            return redirect(url_for("auth.login"))
        return f(*args, **kwargs)
    return decorated


def ban_check(f):
    """Check ban status on every protected request."""
    @wraps(f)
    def decorated(*args, **kwargs):
        if "user_id" in session:
            user = UserModel.get_by_id(session["user_id"])
            if not user or user["statut"] == "banni":
                session.clear()
                flash("Votre compte a été suspendu.", "error")
                return redirect(url_for("auth.login"))
        return f(*args, **kwargs)
    return decorated


@user_bp.route("/dashboard")
@login_required
@ban_check
def dashboard():
    user = UserModel.get_by_id(session["user_id"])
    dernieres_parties = PartieModel.get_last_by_user(session["user_id"], limit=5)
    nb_parties = PartieModel.count_by_user(session["user_id"])
    return render_template("user/dashboard.html", user=user, parties=dernieres_parties, nb_parties=nb_parties)


@user_bp.route("/profile/edit", methods=["GET", "POST"])
@login_required
@ban_check
def edit_profile():
    user = UserModel.get_by_id(session["user_id"])
    errors = []

    if request.method == "POST":
        pseudo = request.form.get("pseudo", "").strip()
        email = request.form.get("email", "").strip().lower()
        new_password = request.form.get("new_password", "")
        confirm_password = request.form.get("confirm_password", "")

        if not pseudo or len(pseudo) < 3:
            errors.append("Le pseudo doit faire au moins 3 caractères.")
        if not email or "@" not in email:
            errors.append("Adresse email invalide.")

        if pseudo != user["pseudo"] and UserModel.pseudo_exists(pseudo):
            errors.append("Ce pseudo est déjà pris.")
        if email != user["email"] and UserModel.email_exists(email):
            errors.append("Cet email est déjà utilisé.")

        if new_password:
            if len(new_password) < 8:
                errors.append("Le nouveau mot de passe doit faire au moins 8 caractères.")
            if new_password != confirm_password:
                errors.append("Les mots de passe ne correspondent pas.")

        if not errors:
            UserModel.update_profile(session["user_id"], pseudo, email)
            if new_password:
                hashed = bcrypt.hashpw(new_password.encode(), bcrypt.gensalt()).decode()
                UserModel.update_password(session["user_id"], hashed)
            session["pseudo"] = pseudo
            flash("Profil mis à jour avec succès.", "success")
            return redirect(url_for("user.dashboard"))

    return render_template("user/profile.html", user=user, errors=errors)


@user_bp.route("/profile/delete", methods=["GET", "POST"])
@login_required
def delete_account():
    if request.method == "POST":
        UserModel.delete(session["user_id"])
        session.clear()
        flash("Votre compte a été supprimé. À bientôt peut-être !", "info")
        return redirect(url_for("main.index"))
    return render_template("user/delete.html")
