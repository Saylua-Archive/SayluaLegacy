from saylua.models.user import User
from saylua.wrappers import login_required

from flask import render_template, redirect, g


# User Profiles
@login_required
def user_profile_default():
    return redirect('/user/' + g.user.name().lower() + '/', code=302)


def user_profile(username):
    user = None
    # TODO address multiple usernames
    if g.logged_in and username.lower() is g.user.name().lower():
        user = g.user
    else:
        user = User.from_username(username)

    # User not found
    if user is None:
        return render_template('notfound.html')

    # Redirect the URL if this is not the main username for the user
    if user.name().lower() != username:
        return redirect('/user/' + user.name().lower() + '/', code=302)

    return render_template('profile/main.html', viewed_user=user)
