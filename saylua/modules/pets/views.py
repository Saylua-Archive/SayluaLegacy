from flask import render_template, redirect
from saylua import db
from .models.db import Pet
from .soul_names import soul_name
from saylua.models.user import User


def pet_profile(name):
    return render_template("profile.html")


def pet_reserve():
    return render_template("reserve.html")


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


def create_pet():
    new_pet = Pet()
    min_length = 5
    new_name = soul_name(min_length)
    found = db.session.query(Pet).filter(Pet.soul_name == new_name).one_or_none()
    while found:
        min_length += 1
        new_name = soul_name(min_length)
        found = db.session.query(Pet).filter(Pet.soul_name == new_name).one_or_none()
    new_pet.soul_name = new_name
    return new_pet
