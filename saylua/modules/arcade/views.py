from flask import render_template

from models.db import Game, GameLog


def games_main():
    return render_template("arcade.html")


def games_blocks():
    game_id = Game("blocks")
    highscores = GameLog.get_highscores(game_id, 10)
    return render_template("blocks.html", game_id=game_id, highscores=highscores)


def games_space():
    return render_template("space.html")
