"""Admin controller — gestion des utilisateurs."""
from functools import wraps
from flask import Blueprint, render_template, request, redirect, url_for, session, flash
import models.user as UserModel
import models.jeu as JeuModel

admin_bp = Blueprint("admin", __name__)


def admin_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if session.get("role") != "admin":
            flash("Accès réservé aux administrateurs.", "error")
            return redirect(url_for("main.index"))
        return f(*args, **kwargs)
    return decorated


def _safe_page(value, default=1):
    try:
        return max(int(value), 1)
    except (TypeError, ValueError):
        return default


def _validate_jeu_form(form):
    nom = form.get("nom", "").strip()
    description = form.get("description", "").strip()
    actif = 1 if form.get("actif") == "1" else 0

    errors = []
    if len(nom) < 2:
        errors.append("Le nom du jeu doit faire au moins 2 caractères.")
    if len(description) < 5:
        errors.append("La description doit faire au moins 5 caractères.")

    try:
        min_joueurs = int(form.get("min_joueurs", "1"))
        max_joueurs = int(form.get("max_joueurs", "1"))
    except ValueError:
        return None, ["Le nombre de joueurs doit être numérique."]

    if min_joueurs < 1 or max_joueurs < 1:
        errors.append("Le nombre de joueurs doit être au minimum 1.")
    if min_joueurs > max_joueurs:
        errors.append("Le minimum de joueurs ne peut pas dépasser le maximum.")

    return {
        "nom": nom,
        "description": description,
        "min_joueurs": min_joueurs,
        "max_joueurs": max_joueurs,
        "actif": actif,
    }, errors


@admin_bp.route("/admin/users")
@admin_required
def list_users():
    search = request.args.get("q", "").strip()
    page = _safe_page(request.args.get("page", 1), 1)
    per_page = 20
    offset = (page - 1) * per_page

    users = UserModel.get_all(search=search, limit=per_page, offset=offset)
    total = UserModel.count_all(search=search)
    total_pages = max((total + per_page - 1) // per_page, 1)

    return render_template(
        "admin/users.html",
        users=users,
        search=search,
        page=page,
        total_pages=total_pages,
    )


@admin_bp.route("/admin/jeux")
@admin_required
def list_jeux():
    search = request.args.get("q", "").strip()
    page = _safe_page(request.args.get("page", 1), 1)
    per_page = 20
    offset = (page - 1) * per_page

    jeux = JeuModel.get_all_paginated(search=search, limit=per_page, offset=offset)
    total = JeuModel.count_all(search=search)
    total_pages = max((total + per_page - 1) // per_page, 1)

    return render_template(
        "admin/jeux.html",
        jeux=jeux,
        search=search,
        page=page,
        total_pages=total_pages,
    )


@admin_bp.route("/admin/jeux/nouveau", methods=["GET", "POST"])
@admin_required
def create_jeu():
    values = {
        "nom": "",
        "description": "",
        "min_joueurs": 1,
        "max_joueurs": 1,
        "actif": 1,
    }
    errors = []

    if request.method == "POST":
        data, errors = _validate_jeu_form(request.form)
        values = data or values
        if not errors:
            JeuModel.create(**data)
            flash("Jeu créé avec succès.", "success")
            return redirect(url_for("admin.list_jeux"))

    return render_template("admin/jeu_form.html", mode="create", values=values, errors=errors)


@admin_bp.route("/admin/jeux/<int:jeu_id>/modifier", methods=["GET", "POST"])
@admin_required
def edit_jeu(jeu_id: int):
    jeu = JeuModel.get_by_id(jeu_id)
    if not jeu:
        flash("Jeu introuvable.", "error")
        return redirect(url_for("admin.list_jeux"))

    values = {
        "nom": jeu["nom"],
        "description": jeu["description"],
        "min_joueurs": jeu["min_joueurs"],
        "max_joueurs": jeu["max_joueurs"],
        "actif": jeu["actif"],
    }
    errors = []

    if request.method == "POST":
        data, errors = _validate_jeu_form(request.form)
        values = data or values
        if not errors:
            JeuModel.update(jeu_id, **data)
            flash("Jeu modifié avec succès.", "success")
            return redirect(url_for("admin.list_jeux"))

    return render_template("admin/jeu_form.html", mode="edit", values=values, errors=errors, jeu_id=jeu_id)


@admin_bp.route("/admin/jeux/<int:jeu_id>/supprimer", methods=["GET", "POST"])
@admin_required
def delete_jeu(jeu_id: int):
    jeu = JeuModel.get_by_id(jeu_id)
    if not jeu:
        flash("Jeu introuvable.", "error")
        return redirect(url_for("admin.list_jeux"))

    if request.method == "POST":
        JeuModel.delete(jeu_id)
        flash(f"Jeu '{jeu['nom']}' supprimé.", "success")
        return redirect(url_for("admin.list_jeux"))

    return render_template("admin/confirm_delete_jeu.html", jeu=jeu)


@admin_bp.route("/admin/users/<int:user_id>/bannir", methods=["POST"])
@admin_required
def bannir(user_id: int):
    user = UserModel.get_by_id(user_id)
    if not user:
        flash("Utilisateur introuvable.", "error")
        return redirect(url_for("admin.list_users"))
    if user["role"] == "admin":
        flash("Impossible de bannir un administrateur.", "error")
        return redirect(url_for("admin.list_users"))

    new_statut = "actif" if user["statut"] == "banni" else "banni"
    UserModel.set_statut(user_id, new_statut)
    action = "débanni" if new_statut == "actif" else "banni"
    flash(f"Utilisateur {user['pseudo']} {action}.", "success")
    return redirect(url_for("admin.list_users"))


@admin_bp.route("/admin/users/<int:user_id>/supprimer", methods=["GET", "POST"])
@admin_required
def supprimer(user_id: int):
    user = UserModel.get_by_id(user_id)
    if not user:
        flash("Utilisateur introuvable.", "error")
        return redirect(url_for("admin.list_users"))
    if user["role"] == "admin":
        flash("Impossible de supprimer un administrateur.", "error")
        return redirect(url_for("admin.list_users"))

    if request.method == "POST":
        UserModel.delete(user_id)
        flash(f"Compte de {user['pseudo']} supprimé.", "success")
        return redirect(url_for("admin.list_users"))

    return render_template("admin/confirm_delete.html", user=user)


@admin_bp.route("/admin/users/<int:user_id>/role", methods=["POST"])
@admin_required
def changer_role(user_id: int):
    user = UserModel.get_by_id(user_id)
    if not user:
        flash("Utilisateur introuvable.", "error")
        return redirect(url_for("admin.list_users"))

    new_role = "admin" if user["role"] == "joueur" else "joueur"
    UserModel.set_role(user_id, new_role)
    flash(f"Rôle de {user['pseudo']} changé en {new_role}.", "success")
    return redirect(url_for("admin.list_users"))
