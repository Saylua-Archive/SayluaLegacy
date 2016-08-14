from saylua import app, login_required
from flask import (render_template, redirect, g,
                   url_for, flash, session, abort, request)

@app.route('/ha/')
@login_required
def ha_customization():
    return render_template("ha/customize.html")

@app.route('/ha/', methods=['POST'])
@login_required
def ha_customization_post():
    if 'img' in request.form:
        flash('Human avatar saved.')
        g.user.ha_url = request.form['img']
        g.user.put()
    return redirect('/ha/')
