from flask import (Blueprint, render_template, redirect,
                   url_for, flash, session, abort, request)

home_module = Blueprint('home_module', __name__)

@home_module.route('/')
def home():
    image_data = {}
    return render_template("index.html", images=image_data, username="")
