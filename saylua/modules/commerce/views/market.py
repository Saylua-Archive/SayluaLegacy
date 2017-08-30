from flask import render_template

from saylua.wrappers import login_required


@login_required()
def market_main():
    return render_template("market/main.html")
