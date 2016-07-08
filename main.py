# Import the Flask Framework
from flask import Flask
import os
import sys


# This is necessary so other directories can find the lib folder
sys.path.append(os.path.join(os.path.dirname(__file__), 'lib'))

# Note: We don't need to call run() since our application is embedded within
# the App Engine WSGI application server.

from os.path import isfile, join
from flask import Blueprint, request, session, g, redirect, url_for, abort, render_template, flash, make_response

app = Flask(__name__)
app.config.from_pyfile('config.py')

@app.errorhandler(404)
def page_not_found(e):
    """Return a custom 404 error."""
    return 'Sorry, nothing at this URL.', 404

@app.errorhandler(500)
def application_error(e):
    """Return a custom 500 error."""
    return 'Sorry, unexpected error: {}'.format(e), 500

# Link up modules
from modules.home import home_module
from modules.login import login_module
from modules.search import search_module
from modules.submit import submit_module

app.register_blueprint(home_module)
app.register_blueprint(login_module)
app.register_blueprint(search_module)
app.register_blueprint(submit_module)
