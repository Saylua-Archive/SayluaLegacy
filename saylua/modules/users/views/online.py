from saylua import app, db

from flask import render_template
from saylua.models.user import User
import datetime


# Users Online
def users_online():
    mins_ago = datetime.datetime.now() - datetime.timedelta(
        minutes=app.config['USERS_ONLINE_RANGE'])
    users = db.session.query(User).filter(User.last_action >= mins_ago)
    return render_template('online.html', users_online=users)
