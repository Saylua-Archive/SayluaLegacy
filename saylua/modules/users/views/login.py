from saylua import app, db

from saylua.models.user import LoginSession, User
from saylua.wrappers import login_required

from ..forms.login import LoginForm, RegisterForm, RecoveryForm, login_check

from flask import render_template, redirect, make_response, request, flash, g

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
        db.session.commit()

        # Generate a matching cookie and redirect
        resp = make_response(redirect('/'))
        resp.set_cookie("session_id", new_session.id, expires=expires)

        return resp

    return render_template('login/login.html', form=form)


def recover_login():
    form = RecoveryForm(request.form)
    return render_template('login/recover.html', form=form)


def reset_password(user, code):
    return render_template('login/recover.html')


@login_required
def logout():
    session_id = request.cookies.get('session_id')
    session = (
        db.session.query(LoginSession)
        .filter(LoginSession.id == session_id)
        .first()
    )

    # Make sure people can't log each other out
    if not session or session.user_id != g.user.id:
        return render_template("403.html"), 403

    if session:
        db.session.delete(session)
        db.session.commit()

    resp = make_response(redirect('/'))
    resp.set_cookie('session_id', '', expires=0)
    return resp


# Registration form shown to the user
def register():
    form = RegisterForm(request.form)

    if request.method == 'POST' and form.validate():
        if (form.invite_code.data != 'cat'):
            flash('The invite code you entered is invalid.', 'error')
            return render_template('login/register.html', form=form)
        username = form.username.data
        password = form.password.data
        email = form.email.data

        phash = User.hash_password(password)
        new_user = User(
            username=username,
            phash=phash,
            email=email
        )

        db.session.add(new_user)
        db.session.commit()

        # Add a session to the datastore
        expires = datetime.datetime.utcnow()
        expires += datetime.timedelta(days=app.config['COOKIE_DURATION'])
        new_session = LoginSession(user_id=new_user.id, expires=expires)

        db.session.add(new_session)
        db.session.commit()

        # Generate a matching cookie and redirct
        resp = make_response(redirect('/'))
        resp.set_cookie('session_id', new_session.id, expires=expires)
        return resp

    return render_template('login/register.html', form=form)
