from saylua import app
from flask import (render_template, redirect,
                   url_for, flash, session, abort, request)

@app.route('/explore/')
def explore_home():
    return render_template("explore/map.html")

@app.route('/battle/')
def explore_battle():
    return render_template("explore/battle.html")
