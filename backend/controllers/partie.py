"""Partie controller — API endpoints + classement."""
import random
from flask import Blueprint, request, jsonify, session, render_template
import models.partie as PartieModel
import models.user as UserModel

partie_bp = Blueprint("partie", __name__)

ROUGE = {1,3,5,7,9,12,14,16,18,19,21,23,25,27,30,32,34,36}

MIS_DEFAUT = 50


def _require_login():
    if "user_id" not in session:
        return jsonify({"error": "Non connecté"}), 401
    return None


@partie_bp.route("/api/partie/save", methods=["POST"])
def save():
    check = _require_login()
    if check:
        return check

    data = request.get_json(silent=True) or {}
    jeu_id = data.get("jeu_id")
    resultat = data.get("resultat")
    points_gagnes = data.get("points_gagnes", 0)

    if jeu_id not in (1, 2, 3) or resultat not in ("gagne", "perdu", "nul"):
        return jsonify({"error": "Données invalides"}), 400

    user_id = session["user_id"]
    user = UserModel.get_by_id(user_id)
    if not user or user["statut"] == "banni":
        return jsonify({"error": "Compte suspendu"}), 403

    UserModel.update_solde(user_id, points_gagnes)
    PartieModel.save(user_id, jeu_id, resultat, points_gagnes)

    new_solde = UserModel.get_by_id(user_id)["solde_points"]
    return jsonify({"ok": True, "new_solde": new_solde})


@partie_bp.route("/api/roulette/jouer", methods=["POST"])
def jouer_roulette():
    check = _require_login()
    if check:
        return check

    data = request.get_json(silent=True) or {}
    mise = int(data.get("mise", MIS_DEFAUT))
    choix = data.get("choix", "")

    user_id = session["user_id"]
    user = UserModel.get_by_id(user_id)
    if not user or user["statut"] == "banni":
        return jsonify({"error": "Compte suspendu"}), 403
    if user["solde_points"] < mise:
        return jsonify({"error": "Solde insuffisant"}), 400

    numero = random.randint(0, 36)
    couleur = "vert" if numero == 0 else ("rouge" if numero in ROUGE else "noir")

    gagne = False
    if choix == "rouge" and couleur == "rouge":
        gagne = True
    elif choix == "noir" and couleur == "noir":
        gagne = True
    elif choix.isdigit() and int(choix) == numero:
        gagne = True

    if gagne:
        if choix in ("rouge", "noir"):
            pts = mise
        else:
            pts = mise * 35
        resultat = "gagne"
    else:
        pts = -mise
        resultat = "perdu"

    UserModel.update_solde(user_id, pts)
    PartieModel.save(user_id, 2, resultat, pts)

    new_solde = UserModel.get_by_id(user_id)["solde_points"]
    return jsonify({
        "numero": numero,
        "couleur": couleur,
        "resultat": resultat,
        "points": pts,
        "new_solde": new_solde,
    })


@partie_bp.route("/classement")
def classement():
    joueurs = PartieModel.classement(limit=20)
    return render_template("classement.html", joueurs=joueurs)
