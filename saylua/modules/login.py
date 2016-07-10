from saylua import app
from flask import (render_template, redirect,
                   url_for, flash, session, abort, request)

@app.route('/login/')
def login():
    return render_template("login/login.html")

@app.route('/login/recover/')
def recover_login():
    return render_template("login/recover.html")

@app.route('/login/reset/<user>/<code>/')
def reset_password(user, code):
    return render_template("login/recover.html")

@app.route('/logout/')
def logout():
    return "Logged out"

@app.route('/register/')
def register():
    return render_template("login/register.html")
