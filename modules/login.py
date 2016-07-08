from flask import (Blueprint, render_template, redirect,
                   url_for, flash, session, abort, request)

login_module = Blueprint('login_module', __name__)

@login_module.route('/login/')
def login():
    return render_template("login.html")

@login_module.route('/login/', methods=['POST'])
def login_post():
    username = request.form['username']
    password = request.form['password']
    return ""

@login_module.route("/logout/")
def logout():
    return ""

@login_module.route("/register/")
def register():
    return render_template("register.html")

@login_module.route("/register/", methods=['POST'])
def register_post():
    return ""
