from saylua import app, login_required
from flask import render_template

from random import randint


@app.route('/explore/')
@login_required
def explore_home():
    return render_template("explore/map.html")


@app.route('/battle/')
@login_required
def explore_battle():
    return render_template("explore/battle.html", bg_num=randint(1, 21))
