from saylua.wrappers import login_required

from flask import render_template, flash, request


@login_required
def customize():
    if request.method == 'POST' and 'img' in request.form:
        flash('Human avatar saved.')
    return render_template("customize.html")
