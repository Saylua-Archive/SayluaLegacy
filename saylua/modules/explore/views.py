from saylua import app
from saylua.wrappers import login_required

from flask import render_template
from random import randint

@login_required
def explore_home():
    return render_template("map.html")


@login_required
def explore_battle():
    return render_template("battle.html", bg_num=randint(1, 21))
