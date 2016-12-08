from saylua import app
from flask import render_template, redirect


def pet_profile(name):
    return render_template("profile.html")


def pet_room(name):
    return render_template("room.html")


def pet_adoption():
    return render_template("adopt.html")


def pet_collection_default():
    username = 'user'
    return redirect('/den/' + username, code=302)


def pet_collection(username):
    return render_template("den.html")
