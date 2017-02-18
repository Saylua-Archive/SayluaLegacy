from saylua import app

from saylua.utils.form import flash_errors
from saylua.models.user import LoginSession, User
from saylua.wrappers import login_required

from ..forms.login import LoginForm, RegisterForm, login_check

from google.appengine.ext import ndb
from flask import render_template, redirect, make_response, request, g

import datetime


@app.context_processor
def inject_sidebar_login_form():
    try:
        if g.logged_in:
            return {}
    except AttributeError:
        g.logged_in = False

    form = LoginForm()
    return dict(sidebar_form=form)


# Login form shown to the user
def login():
    form = LoginForm(request.form)

    if request.method == 'POST' and form.validate():
        found = login_check.user
        found_id = found.id

        # Add a session to the datastore
        expires = datetime.datetime.utcnow()
        expires += datetime.timedelta(days=app.config['COOKIE_DURATION'])
        new_session = LoginSession(user_id=found_id, expires=expires)
        db.session.add(new_session)

        # Generate a matching cookie and redirect
        resp = make_response(redirect('/'))
        resp.set_cookie("session_id", new_session.id, expires=expires)

        return resp

    flash_errors(form)
    return render_template('login/login.html', form=form)


def recover_login():
    return render_template('login/recover.html')


def reset_password(user, code):
    return render_template('login/recover.html')


@login_required
def logout():
    user_key = request.cookies.get('user_key')
    session_key = request.cookies.get('session_key')
    key = ndb.Key(urlsafe=session_key)
    found = key.get()
    if found is not None and found.user_key == user_key:
        found.key.delete()
    resp = make_response(redirect('/'))
    resp.set_cookie('user_key', '', expires=0)
    resp.set_cookie('session_key', '', expires=0)
    return resp


# Registration form shown to the user
def register():
    form = RegisterForm(request.form)

    if request.method == 'POST' and form.validate():
        display_name = form.username.data
        password = form.password.data
        email = form.email.data

        phash = User.hash_password(password)
        new_user = User(
            display_name=display_name,
            phash=phash,
            email=email
        )


        # Add a session to the datastore
        expires = datetime.datetime.utcnow()
        expires += datetime.timedelta(days=app.config['COOKIE_DURATION'])
        new_session = LoginSession(user_key=user_key, expires=expires)
        session_key = new_session.put().urlsafe()

        # Generate a matching cookie and redirct
        resp = make_response(redirect('/'))
        resp.set_cookie('user_key', user_key, expires=expires)
        resp.set_cookie('session_key', session_key, expires=expires)
        return resp

    flash_errors(form)
    return render_template('login/register.html', form=form)
