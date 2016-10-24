from saylua import app, login_required
from flask import (render_template, redirect, g,
                   url_for, flash, session, abort, request)
from saylua.models.user import User

# User Profiles
@app.route('/user/')
@login_required
def user_profile_default():
    return redirect('/user/' + g.user.display_name.lower() + '/', code=302)

@app.route('/user/<username>/')
def user_profile(username):
    user = None
    if g.logged_in and username in g.user.usernames:
        user = g.user
    else:
        user = User.by_username(username)

    # User not found
    if user == None:
        return render_template('user/notfound.html')

    # Redirect the URL if this is not the main username for the user
    if user.display_name.lower() != username:
        return redirect('/user/' + user.display_name.lower() + '/', code=302)

    return render_template('user/profile/main.html', viewed_user=user)
