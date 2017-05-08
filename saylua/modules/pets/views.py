from flask import render_template, g, redirect, request, flash
from saylua import db
from .models.db import Pet
from saylua.models.user import User


def pet_profile(name):
    pet = db.session.query(Pet).filter(Pet.soul_name == name).one_or_none()
    if pet is None:
        return render_template('404.html'), 404
    return render_template("profile.html", pet=pet)


def pet_reserve():
    if request.method == 'POST':
        adopter = g.user
        if not adopter:
            flash("You need to be logged in to adopt a companion!", "error")
            return redirect("/login")
        soul_name = request.form.get('soul_name')
        adoptee = db.session.query(Pet).filter(Pet.soul_name == soul_name).one_or_none()
        if adoptee is None:
            flash("Sorry, I couldn't find a pet with that soul name.")
        elif adoptee.owner_id is not None:
            flash("I'm afraid " + adoptee.name + " already has a companion.")
        else:
            adoptee.owner_id = adopter.id
            adoptee.bonding_date = db.func.now()
            db.session.add(adoptee)
            if adopter.companion is None:
                adopter.companion = adoptee
                db.session.add(adopter)
            db.session.commit()
            flash("You have adopted " + adoptee.name + "!")
            return redirect('/pet/' + soul_name, code=302)
    adoptee = Pet.query.order_by(db.func.random()).first()
    return render_template("reserve.html", adoptee=adoptee)


def pet_collection_default():
    username = "user"
    return redirect("/den/" + username, code=302)


def pet_collection(username):
    user = User.from_username(username)
    # User not found
    if user is None:
        return render_template("404.html"), 404

    pets = (
        db.session.query(Pet)
        .filter(Pet.user_id == user.id)
        .all()
    )
    return render_template("den.html", pets=pets)
