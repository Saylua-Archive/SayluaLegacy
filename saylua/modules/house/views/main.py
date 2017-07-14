from flask import render_template
from saylua.wrappers import login_required


@login_required()
def house():
    return render_template("house_main.html")
