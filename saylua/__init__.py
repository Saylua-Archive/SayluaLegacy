# Import the Flask Framework
# from flask import Flask
from routing import SayluaApp

# Note: We don't need to call run() since our application is embedded within
# the App Engine WSGI application server.

from os.path import join
from flask import send_from_directory, render_template

app = SayluaApp(__name__)
app.config.from_pyfile('config/secure.py')
app.config.from_pyfile('config/settings.py')

import routing
import wrappers
import g_globals
import context_processors
import template_filters

# Populate app with blueprints
enabled_modules = [
    'explore'
]

routing.register_urls(app, enabled_modules)

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
import api
import modules
