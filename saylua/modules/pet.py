from saylua import app
from flask import (render_template, redirect,
                   url_for, flash, session, abort, request)

@app.route('/pet/<name>/')
def pet_profile(name):
    return render_template("pets/profile.html")
