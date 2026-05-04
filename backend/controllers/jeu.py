"""Jeu controller — catalogue des jeux."""
from flask import Blueprint, render_template, session
import models.jeu as JeuModel
import models.partie as PartieModel

jeu_bp = Blueprint("jeu", __name__)


@jeu_bp.route("/jeux")
def catalogue():
    jeux = [
        {"id": j[0], "nom": j[1], "description": j[2]}
        for j in JeuModel.get_main_games_cached()
    ]
    top_joueurs = PartieModel.classement(limit=10)
    return render_template("jeux/catalogue.html", jeux=jeux, top_joueurs=top_joueurs)


@jeu_bp.route("/jeux/blackjack")
def blackjack():
    return render_template("jeux/blackjack.html")


@jeu_bp.route("/jeux/roulette")
def roulette():
    return render_template("jeux/roulette.html")


@jeu_bp.route("/jeux/poker")
def poker():
    return render_template("jeux/bataille.html")


@jeu_bp.route("/jeux/bataille")
def bataille():
    return render_template("jeux/bataille.html")
