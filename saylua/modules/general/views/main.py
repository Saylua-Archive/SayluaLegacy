from flask import render_template, redirect, g, abort, make_response, request

from saylua import app, db
from saylua.utils import is_devserver, redirect_to_referer
from saylua.wrappers import login_required

import datetime


def home():
    try:
        if is_devserver() or g.user:
            return redirect('/news/', code=302)
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
    return render_template("intro/side.html")


@login_required()
def intro_companion():
    return render_template("intro/companion.html")


@login_required()
def intro_avatar():
    return render_template("intro/avatar.html", starter_genus="Chirling")
