from flask import render_template


def npc_shop_view(name):
    return render_template("shops/npc.html")
