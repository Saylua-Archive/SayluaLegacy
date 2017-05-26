from flask import render_template, g, redirect, request, flash
from saylua import db
from saylua.wrappers import login_required, login_required_with_args

from .models.db import Pet

import datetime


def pet_profile(name):
    pet = db.session.query(Pet).filter(Pet.soul_name == name).one_or_none()
    if pet is None:
        return render_template('404.html'), 404
    return render_template("profile.html", pet=pet)


@login_required
def edit_pet(name):
    pet = db.session.query(Pet).filter(Pet.soul_name == name).one_or_none()
    if pet is None:
        return render_template('404.html'), 404
    if pet.owner_id != g.user.id:
        flash("You can't edit {}'s profile!".format(pet.name))
        return redirect('/pet/' + pet.soul_name, code=302)
    return render_template("edit_pet.html", pet=pet)


@login_required
def pet_accompany(soul_name):
    if soul_name:
        companion = db.session.query(Pet).filter(Pet.soul_name == soul_name).one_or_none()
        if companion is None or companion.owner_id != g.user.id:
            flash("You can't accompany this companion.")
        else:
            current_companion = g.user.companion
            if not current_companion:
                g.user.companion_id = companion.id
                flash("{} is now accompanying you!".format(companion.name))
            elif current_companion.id == companion.id:
                g.user.companion_id = None
                flash("{} has gone back to your den.".format(companion.name))
            else:
                g.user.companion_id = companion.id
                flash("{} is now accompanying you! {} has gone back to your den."
                    .format(companion.name, current_companion.name))
            db.session.add(g.user)
            db.session.commit()
    return redirect('/pet/' + companion.soul_name, code=302)


@login_required
def pet_abandon():
    abandon_id = request.form.get('abandonee')
    abandonee = db.session.query(Pet).filter(Pet.id == abandon_id).one_or_none()
    if abandonee is None or abandonee.owner_id != g.user.id:
        flash("You can't abandon this companion.", 'error')
    else:
        if g.user.companion_id == abandonee.id:
            g.user.companion_id = None
            db.session.add(g.user)
            abandonee.owner_id = None
        else:
            abandonee.owner_id = None
        db.session.add(abandonee)
        db.session.commit()
    return redirect('/pet/' + abandonee.soul_name, code=302)


def pet_reserve():
    new_adoptee = Pet.query.filter(Pet.owner_id == None).order_by(db.func.random()).first() # noqa
    if new_adoptee is None:
        return render_template("reserve_empty.html")
    return render_template("reserve.html", adoptee=new_adoptee)


@login_required_with_args(redirect='pets.reserve', error='You need to be logged in to adopt a companion!')
def pet_reserve_post():
    adopter = g.user
    soul_name = request.form.get('soul_name')
    adoptee = db.session.query(Pet).filter(Pet.soul_name == soul_name).one_or_none()
    youngest = (Pet.query.filter(Pet.owner_id == g.user.id)
            .order_by(Pet.date_bonded.desc()).first())
    if youngest and (datetime.datetime.now() - youngest.date_bonded).days < 1:
        flash(("I'm afraid I can't let you adopt adopt a new companion today, " +
            "you should focus on making sure {} is settling into their new home.")
            .format(youngest.name))
    elif adoptee is None:
        flash("Sorry, I couldn't find a pet with that soul name.")
    elif adoptee.owner_id is not None:
        flash("I'm afraid {} already has a companion.".format(adoptee.name))
    else:
        adoptee.owner_id = adopter.id
        adoptee.date_bonded = db.func.now()
        db.session.add(adoptee)
        if adopter.companion is None:
            adopter.companion = adoptee
            db.session.add(adopter)
        db.session.commit()
        flash("You have adopted {}!".format(adoptee.name))
        return redirect(adoptee.url(), code=302)
    return redirect('/reserve/', code=302)


def species_guide():
    return render_template('species_guide.html')
