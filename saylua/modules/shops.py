from saylua import app
from flask import (render_template, redirect,
                   url_for, flash, session, abort, request)

@app.route('/shop/<name>/')
def npc_shop_view(name):
    return render_template("shops/npc.html")

@app.route('/usershop/<username>/')
def user_shop_view(username):
    return render_template("shops/user.html")
