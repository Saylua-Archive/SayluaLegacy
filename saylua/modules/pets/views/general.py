from flask import render_template, g, redirect, request, flash, abort
from saylua import db
from saylua.wrappers import login_required
from ..forms import PetEditForm, MiniEditForm

from ..models.db import Pet


def pet_profile(soul_name):
    pet = db.session.query(Pet).filter(Pet.soul_name == soul_name).one_or_none()
    if pet is None:
        abort(404)
    mini_form = MiniEditForm(request.form, obj=pet.mini_friendship)
    return render_template("profile.html", pet=pet, mini_form=mini_form)


@login_required()
def edit_pet(soul_name):
    pet = db.session.query(Pet).filter(Pet.soul_name == soul_name).one_or_none()
    if pet is None:
        abort(404)
    if pet.guardian_id != g.user.id:
        flash("You can't edit {}'s profile!".format(pet.name))
        return redirect(pet.url(), code=302)
    form = PetEditForm(request.form, obj=pet)
    if form.validate_on_submit():
        form.populate_obj(pet)
        db.session.commit()
        flash("Your settings have been saved.")
        return redirect(pet.url(), code=302)
    return render_template("edit_pet.html", pet=pet, form=form)


@login_required()
def edit_mini(soul_name):
    pet = db.session.query(Pet).filter(Pet.soul_name == soul_name).one_or_none()
    if pet is None:
        abort(404)
    if pet.guardian_id != g.user.id:
        flash("You can't edit {}'s mini!".format(pet.name))
        return redirect(pet.url(), code=302)
    form = MiniEditForm(request.form, obj=pet.mini_friendship)
    if form.validate_on_submit():
        form.populate_obj(pet.mini_friendship)
        db.session.commit()
        flash("The settings for you mini have been saved.")
        return redirect(pet.url(), code=302)
    return render_template('edit_mini.html', pet=pet, form=form)


@login_required()
def pet_accompany(soul_name):
    if soul_name:
        companion = db.session.query(Pet).filter(Pet.soul_name == soul_name).one_or_none()
        if companion is None or companion.guardian_id != g.user.id:
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


@login_required()
def pet_abandon():
    abandon_id = request.form.get('abandonee')
    abandonee = db.session.query(Pet).filter(Pet.id == abandon_id).one_or_none()
    if abandonee is None or abandonee.guardian_id != g.user.id:
        flash("You can't abandon this companion.", 'error')
    else:
        if g.user.companion_id == abandonee.id:
            g.user.companion_id = None
            db.session.add(g.user)
            abandonee.guardian_id = None
        else:
            abandonee.guardian_id = None
        db.session.add(abandonee)
        db.session.commit()
    return redirect('/pet/' + abandonee.soul_name, code=302)


def species_guide():
    return render_template('species_guide.html')
