from saylua import app, login_required
from flask import (render_template, redirect, make_response,
                   url_for, flash, session, abort, request, g)
from google.appengine.ext import ndb
import random, string
from bcryptmaster import bcrypt
import datetime, re

from saylua.models.user import LoginSession, User

@app.route('/login/', methods=['GET'])
def login():
    return render_template("login/login.html")

@app.route('/login/', methods=['POST'])
def login_post():
    username = request.form['username'].lower()
    password = request.form['password']

    found = User.query(User.username == username).get()
    if found == None:
        flash("We can't find a user by that name.", 'error')
        return render_template("login/login.html")

    if not bcrypt.hashpw(password, found.phash) == found.phash:
        flash("Your password is incorrect.", 'error')
        return render_template("login/login.html")

    #found_key = User.query(User.username == username).get(keys_only=True).urlsafe()
    found_key = found.key.urlsafe()

    #Add a session to the datastore
    session_key = ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(32))
    expires = datetime.datetime.utcnow()
    expires += datetime.timedelta(days=app.config['COOKIE_DURATION'])
    new_session = LoginSession(user_key=found_key, session_key=session_key,
            expires=expires)
    new_session.put()

    #Generate a matching cookie and redirct
    resp = make_response(redirect(url_for('home')))
    resp.set_cookie("user_key", found_key, expires=expires)
    resp.set_cookie("session_key", session_key, expires=expires)
    return resp


@app.route('/login/recover/')
def recover_login():
    return render_template("login/recover.html")

@app.route('/login/reset/<user>/<code>/')
def reset_password(user, code):
    return render_template("login/recover.html")

@app.route('/logout/')
def logout():
    user_key = request.cookies.get('user_key')
    session_key = request.cookies.get('session_key')
    found = LoginSession.query(LoginSession.user_key == user_key,
        LoginSession.session_key == session_key).get()
    if found != None:
        found.key.delete()
    resp = make_response(redirect(url_for('home')))
    resp.set_cookie('user_key', '', expires=0)
    resp.set_cookie('session_key', '', expires=0)
    return resp

@app.route('/register/', methods=['GET'])
def register():
    return render_template("login/register.html")

@app.route('/register/', methods=['POST'])
def register_post():
    display_name = request.form['username']
    username = display_name.lower()
    password = request.form['password']
    password2 = request.form['password2']
    email = request.form['email'].lower()
    tos_agreed = 'tos_agreed' in request.form

    valid = True
    #Validate everything here
    if password != password2:
        flash("Passwords must match!", 'error')
        valid = False

    if username == None or password == None or email == None:
        flash("You're missing a field!", 'error')
        valid = False

    if not tos_agreed:
        flash("You must accept the TOS to register.", 'error')
        valid = False

    if len(password) < app.config['MIN_PASSWORD_LENGTH']:
        flash("Your password must be at least " + str(app.config['MIN_PASSWORD_LENGTH']) + " characters.", 'error')
        valid = False

    if len(username) < app.config['MIN_USERNAME_LENGTH']:
        flash("Your password must be at least " + str(app.config['MIN_USERNAME_LENGTH']) + " characters.", 'error')
        valid = False

    if len(email) < 5:
        flash("You must use a valid email address.", 'error')
        valid = False

    pattern = re.compile('^[A-Za-z0-9_-]*$')
    if not pattern.match(username):
        flash("Your username may only contain letters, numbers, underscores, or hyphens.", 'error')
        valid = False

    if not valid:
        return redirect(url_for('register'))

    found = User.query(User.username == username).get()
    if found != None:
        valid = False
        flash("A user with that username already exists.", 'error')
    if valid:
        phash = bcrypt.hashpw(password, bcrypt.gensalt())
        new_user = User(username=username, display_name=display_name, phash=phash,
                email=email, email_verified=False)
        user_key = new_user.put().urlsafe()

        #Add a session to the datastore
        session_key = ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(32))
        expires = datetime.datetime.utcnow()
        expires += datetime.timedelta(days=app.config['COOKIE_DURATION'])
        new_session = LoginSession(user_key=user_key, session_key=session_key,
                expires=expires)
        new_session.put()

        #Generate a matching cookie and redirct
        resp = make_response(redirect(url_for('home')))
        resp.set_cookie("user_key", user_key, expires=expires)
        resp.set_cookie("session_key", session_key, expires=expires)
        return resp

    return redirect(url_for('register'))
