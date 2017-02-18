# flake8: noqa
from .routing import SayluaApp

# Note: We don't need to call run() since our application is embedded within
# the App Engine WSGI application server.

from os.path import join
from flask import send_from_directory, render_template
from flask_sqlalchemy import SQLAlchemy
from saylua.utils import is_devserver

app = SayluaApp(__name__)
app.config.from_pyfile('config/secure.py')
app.config.from_pyfile('config/settings.py')
if is_devserver():
    app.config.from_pyfile('config/local_settings.py')

db = SQLAlchemy(app)

from . import (
    context_processors,
    g_globals,
    routing,
    template_filters,
    wrappers,
)

# Populate app with blueprints
enabled_modules = [
    'admin',
    'arcade',
    'avatar',
    'books',
    'explore',
    'forums',
    'home',
    'items',
    'messages',
    'pets',
    'search',
    'trade',
    'users',
    'world'
]

routing.register_urls(app, enabled_modules)

with app.app_context():
    db.create_all()


@app.route('/favicon.ico')
def favicon():
    return send_from_directory(join(app.root_path, 'static'), 'favicon.ico',
        mimetype='image/vnd.microsoft.icon')


@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404


@app.errorhandler(500)
def application_error(e):
    return render_template("500.html"), 500


# Make sure imports for other modules are at the bottom of the file
import modules
