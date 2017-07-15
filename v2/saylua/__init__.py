# Note: We don't need to call run() since our application is embedded within
# the App Engine WSGI application server.

from flask import Flask, render_template
from flask_wtf.csrf import CSRFProtect

from flask_sqlalchemy import SQLAlchemy
from saylua.utils import is_devserver
from google.appengine.api import app_identity

app = Flask(__name__)
app.config.from_pyfile('config/secure.py')
app.config.from_pyfile('config/settings.py')

if app_identity.get_application_id() == "saylua-staging":
    app.config.from_pyfile('config/secure_staging.py')
if is_devserver():
    app.config.from_pyfile('config/local_settings.py')

db = SQLAlchemy(app)
csrf = CSRFProtect(app)

with app.app_context():
    db.create_all()


@app.route('/')
def main():
    return render_template('main.html')
