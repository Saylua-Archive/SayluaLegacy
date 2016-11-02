from saylua import app, login_required
from flask import (render_template, redirect, make_response,
                   url_for, flash, session, abort, request, g)
from google.appengine.ext import ndb
import random, string
import datetime

from saylua.utils.form import flash_errors
from saylua.models.user import LoginSession, User
from forms.login import LoginForm, RegisterForm, login_check

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
@app.route('/login/', methods=['GET', 'POST'])
def login():
    form = LoginForm(request.form)

    if request.method == 'POST' and form.validate():
        found = login_check.user
        found_key = found.key.urlsafe()

        #Add a session to the datastore
        expires = datetime.datetime.utcnow()
        expires += datetime.timedelta(days=app.config['COOKIE_DURATION'])
        new_session = LoginSession(user_key=found_key, expires=expires)
        session_key = new_session.put().urlsafe()

        #Generate a matching cookie and redirct
        resp = make_response(redirect(url_for('home')))
        resp.set_cookie("user_key", found_key, expires=expires)
        resp.set_cookie("session_key", session_key, expires=expires)

        return resp

    flash_errors(form)
    return render_template('user/login/login.html', form=form)


@app.route('/login/recover/')
def recover_login():
    return render_template('user/login/recover.html')

@app.route('/login/reset/<user>/<code>/')
def reset_password(user, code):
    return render_template('user/login/recover.html')

@app.route('/logout/')
def logout():
    user_key = request.cookies.get('user_key')
    session_key = request.cookies.get('session_key')
    key = ndb.Key(urlsafe=session_key)
    found = key.get()
    if found != None and found.user_key == user_key:
        found.key.delete()
    resp = make_response(redirect(url_for('home')))
    resp.set_cookie('user_key', '', expires=0)
    resp.set_cookie('session_key', '', expires=0)
    return resp

# Registration form shown to the user
@app.route('/register/', methods=['GET', 'POST'])
def register():
    form = RegisterForm(request.form)
    if request.method == 'POST' and form.validate():
        display_name = form.username.data
        username = display_name.lower()
        password = form.password.data
        email = form.email.data

        phash = User.hash_password(password)
        new_user = User(display_name=display_name, usernames=[username], phash=phash,
                email=email)
        user_key = new_user.put().urlsafe()

        # Add a session to the datastore
        expires = datetime.datetime.utcnow()
        expires += datetime.timedelta(days=app.config['COOKIE_DURATION'])
        new_session = LoginSession(user_key=user_key, expires=expires)
        session_key = new_session.put().urlsafe()

        # Generate a matching cookie and redirct
        resp = make_response(redirect(url_for('home')))
        resp.set_cookie('user_key', user_key, expires=expires)
        resp.set_cookie('session_key', session_key, expires=expires)
        return resp
    flash_errors(form)
    return render_template('user/login/register.html', form=form)
