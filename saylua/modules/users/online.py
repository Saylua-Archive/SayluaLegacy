from saylua import app
from flask import render_template
from saylua.models.user import User
import datetime


# Users Online
def users_online():
    mins_ago = datetime.datetime.now() - datetime.timedelta(
        minutes=app.config['USERS_ONLINE_RANGE'])
    users = User.query(User.last_action >= mins_ago).fetch()
    return render_template('online.html', users_online=users)
