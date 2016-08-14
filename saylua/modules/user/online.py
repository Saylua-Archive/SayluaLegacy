from saylua import app, login_required
from flask import (render_template, redirect, g,
                   url_for, flash, session, abort, request)
from saylua.models.user import User

# Users Online
@app.route('/online/')
def users_online():
    return render_template('user/online.html')
