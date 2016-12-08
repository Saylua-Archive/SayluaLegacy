from saylua import app
from flask import render_template


def games_main():
    return render_template("main.html")
