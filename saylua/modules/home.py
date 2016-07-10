from saylua import app
from flask import (render_template, redirect,
                   url_for, flash, session, abort, request)

@app.route('/')
def home():
    return render_template("pages/index.html")
