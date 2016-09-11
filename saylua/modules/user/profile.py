from saylua import app, login_required
from flask import (render_template, redirect, g,
                   url_for, flash, session, abort, request)
from saylua.models.user import User

# User Profiles
@app.route('/user/')
@login_required
def user_profile_default():
    return redirect('/user/' + g.user.username + '/', code=302)

@app.route('/user/<username>/')
def user_profile(username):
    user = None
    if g.logged_in and username == g.user.username:
        user = g.user
    else:
        user = User.by_username(username)

    if user == None:
        return render_template('user/notfound.html')

    return render_template('user/profile/main.html', viewed_user=user)
