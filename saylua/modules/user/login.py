from saylua import app, login_required
from flask import (render_template, redirect, make_response,
                   url_for, flash, session, abort, request, g)
from google.appengine.ext import ndb
import random, string
import datetime

from saylua.utils.validation import FieldValidator
from saylua.models.user import LoginSession, User

@app.route('/login/', methods=['GET'])
def login():
    return render_template('user/login/login.html')

@app.route('/login/', methods=['POST'])
def login_post():
    username = request.form['username'].lower()
    password = request.form['password']

    found = User.by_username(username)
    if found == None:
        flash("We can't find a user by that name.", 'error')
        return render_template('user/login/login.html')

    if not User.check_password(found, password):
        flash("Your password is incorrect.", 'error')
        return render_template('user/login/login.html')

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

@app.route('/register/', methods=['GET'])
def register():
    return render_template('user/login/register.html',
        min_password_length = app.config['MIN_PASSWORD_LENGTH'],
        max_password_length = app.config['MAX_PASSWORD_LENGTH'],
        min_username_length = app.config['MIN_USERNAME_LENGTH'],
        max_username_length = app.config['MAX_USERNAME_LENGTH'])

@app.route('/register/', methods=['POST'])
def register_post():
    display_name = request.form['username']
    username = display_name.lower()
    password = request.form['password']
    password2 = request.form['password2']
    email = request.form['email'].lower()
    tos_agreed = 'tos_agreed' in request.form

    # Validate all of the fields
    passwordValidator = (FieldValidator('password', password)
        .required()
        .min(app.config['MIN_PASSWORD_LENGTH'])
        .max(app.config['MAX_PASSWORD_LENGTH'])
        .matches(password2, error='Passwords must match.'))

    usernameValidator = (FieldValidator('username', username)
        .required()
        .min(app.config['MIN_USERNAME_LENGTH'])
        .max(app.config['MAX_USERNAME_LENGTH'])
        .matches_regex('^[A-Za-z0-9_-]*$', error='Usernames may only contain alphanumeric characters, underscroes, and hyphens.'))

    emailValidator = (FieldValidator('email', email)
        .required()
        .min(5, error='You must enter a valid email address.'))

    tosValidator = (FieldValidator('TOS', tos_agreed)
        .required(error='You must agree to the Terms of Service.'))

    # Flash all of the validation errors found
    passwordValidator.flash()
    usernameValidator.flash()
    emailValidator.flash()
    tosValidator.flash()

    valid = (passwordValidator.valid and usernameValidator.valid
        and emailValidator.valid and tosValidator.valid)

    if not valid:
        return redirect(url_for('register'))

    found = User.key_by_username(username)
    if found != None:
        valid = False
        flash('A user with that username already exists.', 'error')
    if valid:
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

    return redirect(url_for('register'))
