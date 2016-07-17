# Import the Flask Framework
from flask import Flask

# Note: We don't need to call run() since our application is embedded within
# the App Engine WSGI application server.

from os.path import isfile, join
from flask import request, session, g, redirect, url_for, abort, render_template, flash, make_response

app = Flask(__name__)
app.config.from_pyfile('config.py')


@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404

@app.errorhandler(500)
def application_error(e):
    return render_template("500.html"), 500

# Make sure imports for other modules are at the bottom of the file
import api

import modules
