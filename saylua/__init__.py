# Import the Flask Framework
from flask import Flask

# Note: We don't need to call run() since our application is embedded within
# the App Engine WSGI application server.

from os.path import isfile, join
from flask import (request, session, g, redirect, url_for, abort, render_template,
    flash, make_response, send_from_directory)
from functools import wraps

app = Flask(__name__)
app.config.from_pyfile('config/secure.py')
app.config.from_pyfile('config/settings.py')

import g_globals
import context_processors
import template_filters

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if g.logged_in == False:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(join(app.root_path, 'static'),
        'favicon.ico', mimetype='image/vnd.microsoft.icon')

@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404

@app.errorhandler(500)
def application_error(e):
    return render_template("500.html"), 500

# Make sure imports for other modules are at the bottom of the file
import api
import modules
