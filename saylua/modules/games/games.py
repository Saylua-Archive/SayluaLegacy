from saylua import app
from flask import render_template


@app.route('/games/')
def games_main():
    return render_template("games/main.html")
