from saylua.wrappers import login_required
from saylua import db

from flask import render_template, g, flash, request


@login_required
def customize():
    if request.method == 'POST' and 'img' in request.form:
        flash('Human avatar saved.')
        g.user.ha_url = request.form['img']
        db.session.commit()
    return render_template("customize.html")
