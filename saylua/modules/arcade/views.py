from flask import render_template


def games_main():
    return render_template("main.html")


def games_blocks():
    return render_template("blocks.html")


def games_space():
    return render_template("space.html")
