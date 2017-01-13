from flask import render_template

from models.db import GameScore


def games_main():
    return render_template("main.html")


def games_blocks():
    return render_template("blocks.html")


def games_space():
    highscores = GameScore.get_highscores(Game.LINE_BLOCKS, 10)
    return render_template("space.html", highscores=highscores)
