from flask import render_template, g, redirect, request, flash
from saylua import db
from .models.db import Pet


def pet_profile(name):
    pet = db.session.query(Pet).filter(Pet.soul_name == name).one_or_none()
    if pet is None:
        return render_template('404.html'), 404
    return render_template("profile.html", pet=pet)


def pet_accompany():
    if not g.user:
        flash("You need to be logged in to do this!", "error")
        return redirect("/login")
    companion_id = request.form.get('accompany')
    if companion_id:
        companion = db.session.query(Pet).filter(Pet.id == companion_id).one_or_none()
        if companion is None or companion.owner_id != g.user.id:
            flash("You can't accompany this companion.")
        else:
            current_companion = g.user.companion
            if not current_companion:
                g.user.companion_id = companion.id
                flash(companion.name + " is now accompanying you!")
            elif current_companion.id == companion.id:
                g.user.companion_id = None
                flash(companion.name + " has gone back to your den.")
            else:
                g.user.companion_id = companion.id
                flash(companion.name + " is now accompanying you! " +
                    current_companion.name + " has gone back to your den.")
            db.session.add(g.user)
            db.session.commit()
    return redirect('/pet/' + companion.soul_name, code=302)


def pet_abandon():
    if not g.user:
        flash("You need to be logged in to do this!", "error")
        return redirect("/login")
    abandon_id = request.form.get('abandonee')
    abandonee = db.session.query(Pet).filter(Pet.id == abandon_id).one_or_none()
    if abandonee is None or abandonee.owner_id != g.user.id:
        flash("You can't abandon this companion.")
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
    new_adoptee = Pet.query.filter(Pet.owner_id == None).order_by(db.func.random()).first() # noqa
    if new_adoptee is None:
        flash("The adoption center is currently empty! Everyone has found a happy home!")
        return redirect('/news/', code=302)
    return render_template("reserve.html", adoptee=new_adoptee)
