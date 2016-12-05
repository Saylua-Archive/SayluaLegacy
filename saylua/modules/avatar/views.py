from saylua import app
from saylua.wrappers import login_required

from flask import render_template, g, flash, request


@login_required
def customize():
    if request.method == 'POST' and 'img' in request.form:
        flash('Human avatar saved.')
        g.user.ha_url = request.form['img']
        g.user.put()
    return render_template("customize.html")
