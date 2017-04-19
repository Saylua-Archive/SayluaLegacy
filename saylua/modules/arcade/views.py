from flask import render_template

from models.db import Game, GameLog


def games_main():
    return render_template("main.html")


def games_blocks():
    highscores = GameLog.get_highscores(Game("LINE_BLOCKS"), 10)
    return render_template("blocks.html", highscores=highscores)


def games_space():
    return render_template("space.html")
