from saylua import app
from flask import render_template


def npc_shop_view(name):
    return render_template("shops/npc.html")


def user_shop_view(username):
    return render_template("shops/user.html")
