from flask import render_template, redirect
from saylua import db
from .models.db import Pet
from saylua.models.user import User


def pet_profile(name):
    return render_template("profile.html")


def pet_reserve():
    adoptee = Pet.query.order_by(db.func.random()).first()
    return render_template("reserve.html", adoptee)


def pet_collection_default():
    username = 'user'
    return redirect('/den/' + username, code=302)


def pet_collection(username):
    user = User.from_username(username)
    # User not found
    if user is None:
        return render_template('notfound.html')

    pets = (
        db.session.query(Pet)
        .filter(Pet.user_id == user.id)
        .all()
    )
    return render_template("den.html", pets=pets)
