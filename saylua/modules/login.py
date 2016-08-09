from saylua import app
from flask import (render_template, redirect, make_response,
                   url_for, flash, session, abort, request, g)
from google.appengine.ext import ndb
import random, string
from bcryptmaster import bcrypt
import datetime, re
from functools import wraps

from saylua.models.user import LoginSession, User


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        username = request.cookies.get('username')
        session_key = request.cookies.get('session_key')
        found = LoginSession.query(LoginSession.username == username,
                LoginSession.session_key == session_key).get()
        if found == None:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

@app.route('/login/', methods=['GET'])
def login():
    return render_template("login/login.html")

@app.route('/login/', methods=['POST'])
def login_post():
    username = request.form['username'].lower()
    password = request.form['password']

    found = User.query(User.username == username).get()
    if found == None:
        flash("We can't find a user by that name.")
        return render_template("login/login.html")

    if not bcrypt.hashpw(password, found.phash) == found.phash:
        flash("Your password is incorrect.")
        return render_template("login/login.html")

    #Add a session to the datastore
    session_key = ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(32))
    expires = datetime.datetime.utcnow()
    expires += datetime.timedelta(days=app.config['COOKIE_DURATION'])
    new_session = LoginSession(username=found.username, session_key=session_key,
            expires=expires)
    new_session.put()

    #Generate a matching cookie and redirct
    resp = make_response(redirect(url_for('home')))
    resp.set_cookie("username", username, expires=expires)
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
    username = request.cookies.get('username')
    session_key = request.cookies.get('session_key')
    found = LoginSession.query(LoginSession.username == username,
        LoginSession.session_key == session_key).get()
    if found != None:
        found.key.delete()
    resp = make_response(redirect(url_for('home')))
    resp.set_cookie('username', '', expires=0)
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
        flash("Passwords must match!")
        valid = False

    if username == None or password == None or email == None:
        flash("You're missing a field!")
        valid = False

    if not tos_agreed:
        flash("You must accept the TOS to register.")
        valid = False

    if len(password) < app.config['MIN_PASSWORD_LENGTH']:
        flash("Your password must be at least " + str(app.config['MIN_PASSWORD_LENGTH']) + " characters.")
        valid = False

    if len(username) < app.config['MIN_USERNAME_LENGTH']:
        flash("Your password must be at least " + str(app.config['MIN_USERNAME_LENGTH']) + " characters.")
        valid = False

    if len(email) < 5:
        flash("You must use a valid email address.")
        valid = False

    pattern = re.compile('^[A-Za-z0-9_-]*$')
    if not pattern.match(username):
        flash("Your username may only contain letters, numbers, underscores, or hyphens.")
        valid = False

    if not valid:
        return redirect(url_for('register'))

    found = User.query(User.username == username).get()
    if found != None:
        valid = False
        flash("A user with that username already exists.")
    if valid:
        phash = bcrypt.hashpw(password, bcrypt.gensalt())
        new_user = User(username=username, display_name=display_name, phash=phash,
                email=email, email_verified=False)
        new_user.put()

        #Add a session to the datastore
        session_key = ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(32))
        expires = datetime.datetime.utcnow()
        expires += datetime.timedelta(days=app.config['COOKIE_DURATION'])
        new_session = LoginSession(username=username, session_key=session_key,
                expires=expires)
        new_session.put()

        #Generate a matching cookie and redirct
        resp = make_response(redirect(url_for('home')))
        resp.set_cookie("username", username, expires=expires)
        resp.set_cookie("session_key", session_key, expires=expires)
        return resp

    return redirect(url_for('register'))
