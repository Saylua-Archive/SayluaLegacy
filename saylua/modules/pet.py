from saylua import app
from flask import (render_template, redirect,
                   url_for, flash, session, abort, request)

@app.route('/pet/<name>/')
def pet_profile(name):
    return render_template("pets/profile.html")

@app.route('/pets/')
def pet_collection_default():
    username = 'user'
    return redirect('/pets/' + username, code=302)

@app.route('/pets/<username>/')
def pet_collection(username):
    return render_template("pets/profile.html")
