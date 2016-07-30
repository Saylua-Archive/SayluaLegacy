from saylua import app
from flask import (render_template, redirect,
                   url_for, flash, session, abort, request)

@app.route('/pet/<name>/')
def pet_profile(name):
    return render_template("pets/profile.html")

@app.route('/adopt/')
def pet_adoption():
    return render_template("pets/adopt.html")

@app.route('/den/')
def pet_collection_default():
    username = 'user'
    return redirect('/den/' + username, code=302)

@app.route('/den/<username>/')
def pet_collection(username):
    return render_template("pets/den.html")
