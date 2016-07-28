from saylua import app
from flask import (render_template, redirect,
                   url_for, flash, session, abort, request)

@app.route('/ha/')
def ha_customization():
    return render_template("ha/customize.html")
