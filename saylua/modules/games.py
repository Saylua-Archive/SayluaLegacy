from saylua import app
from flask import (render_template, redirect,
                   url_for, flash, session, abort, request)

@app.route('/games/')
def games_main():
    return render_template("games/main.html")
