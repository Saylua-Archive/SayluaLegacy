from saylua import app, login_required
from flask import (render_template, redirect,
                   url_for, flash, session, abort, request)

@app.route('/ha/')
@login_required
def ha_customization():
    return render_template("ha/customize.html")
