from saylua import app, login_required
from flask import (render_template, redirect, g,
                   url_for, flash, session, abort, request)
from saylua.models.user import User
import datetime

# Users Online
@app.route('/online/')
def users_online():
    mins_ago = datetime.datetime.now() - datetime.timedelta(minutes=app.config['USERS_ONLINE_RANGE'])
    users = User.query(User.last_action >= mins_ago).fetch()
    return render_template('user/online.html', users_online=users)
