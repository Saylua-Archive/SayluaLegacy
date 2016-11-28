from saylua import app
from flask import render_template


@app.route('/shop/<name>/')
def npc_shop_view(name):
    return render_template("shops/npc.html")


@app.route('/usershop/<username>/')
def user_shop_view(username):
    return render_template("shops/user.html")
