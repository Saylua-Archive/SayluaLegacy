from flask import (render_template, redirect, g, abort, make_response,
    request, url_for, flash)

from saylua import app, db
from saylua.utils import is_devserver, redirect_to_referer
from saylua.wrappers import login_required
from saylua.modules.pets.models.db import SpeciesCoat, Pet, PetFriendship

import datetime


STARTER_COMPANIONS = ['arko_common', 'chirling_common', 'xochi_common']


def home():
    try:
        if is_devserver() or g.logged_in:
            return redirect('/house/', code=302)
        return landing()
    except AttributeError:
        return landing()


def landing():
    return render_template("landing.html")


def view_page(template):
    template_name = "pages/" + template + ".html"

    try:
        return render_template(template_name)
    except:
        abort(404)


def change_theme():
    try:
        theme_id = int(request.form.get('theme_id'))
    except:
        abort(400)
    response = make_response(redirect_to_referer('general.home'))
    if not g.logged_in:
        expires = datetime.datetime.utcnow()
        expires += datetime.timedelta(days=app.config['COOKIE_DURATION'])
        response.set_cookie("theme_id", str(theme_id), expires=expires)
    else:
        g.user.theme_id = theme_id
        db.session.commit()
    return response


def banned():
    if not (g.logged_in and g.user.is_banned()):
        abort(404)
    return render_template("banned.html")


@login_required()
def intro_side():
    if request.method == 'POST':
        side_id = request.form.get('side_id')
        try:
            side_id = int(side_id)
        except:
            flash('Invalid side format entered.', 'error')

        if side_id < 0 or side_id > 1:
            flash('Invalid side selected.', 'error')
        else:
            g.user.side_id = side_id
            g.user.story_level = 1
            db.session.add(g.user)
            db.session.commit()
            flash("You've decided to move to Saylua %s. A wonderful choice!" % g.user.side_name())
            return redirect(url_for(g.user.story_route()))
    return render_template("intro/side.html")


@login_required()
def intro_companion():
    if g.user.story_level < 1:
        return redirect(url_for(g.user.story_route()))

    starter_list = []
    for canon_name in STARTER_COMPANIONS:
        starter_list.append(SpeciesCoat.by_canon_name(canon_name))

    if request.method == 'POST':
        starter_choice = request.form.get('starter_choice')
        if starter_choice in STARTER_COMPANIONS:
            i = STARTER_COMPANIONS.index(starter_choice)
            starter_coat = starter_list[i]
            companion = Pet(coat_id=starter_coat.id, guardian_id=g.user.id)
            g.user.story_level = 2
            g.user.companion = companion
            db.session.add(companion)
            db.session.commit()

            flash("With your trusty %s, you'll surely be ready to take on the world." % starter_coat.species.name)
            return redirect(url_for(g.user.story_route()))
        else:
            flash('Sorry, that is not a valid starter companion.', 'error')
    return render_template("intro/companion.html", starter_list=starter_list)


@login_required()
def intro_avatar():
    if g.user.story_level < 2:
        return redirect(url_for(g.user.story_route()))

    starter = g.user.companion
    if not starter:
        starter = (Pet.query.filter(Pet.guardian_id == g.user.id)
                .join(PetFriendship.bonding_day)
                .order_by(PetFriendship.bonding_day.asc()).first())
    if request.method == 'POST':
        g.user.story_level = 3
        db.session.commit()

        party_text = "you"
        if starter:
            party_text += " and " + starter.name
        flash("Awesome, you're all geared up and ready to go! It's time for %s to see your new house." % party_text)
        return redirect('/')
    return render_template("intro/avatar.html", starter=starter)
