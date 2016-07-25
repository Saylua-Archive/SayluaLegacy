from saylua import app
from flask import (render_template, redirect,
                   url_for, flash, session, abort, request)

@app.route('/user/<user>/')
def user_profile(user):
    return render_template("user/profile.html")

@app.route('/settings/')
def user_settings():
    return render_template("user/settings/main.html")

@app.route('/settings/profile/')
def user_settings_profile():
    return render_template("user/settings/profile.html")

@app.route('/settings/css/')
def user_settings_css():
    return render_template("user/settings/css.html")

@app.route('/settings/username/')
def user_settings_username():
    return render_template("user/settings/username.html")

@app.route('/settings/email/')
def user_settings_email():
    return render_template("user/settings/email.html")

@app.route('/settings/password/')
def user_settings_password():
    return render_template("user/settings/password.html")
