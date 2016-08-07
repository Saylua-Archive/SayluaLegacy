from saylua import app
from flask import (render_template, redirect,
                   url_for, flash, session, abort, request)
from login import login_required

@app.route('/ha/')
@login_required
def ha_customization():
    return render_template("ha/customize.html")
