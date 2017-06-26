from saylua.modules.users.models.db import User
from saylua.wrappers import login_required

from flask import render_template, redirect, g


# User Profiles
@login_required()
def user_profile_default():
    return redirect(g.user.url(), code=302)


def user_profile(username):
    user = None
    # TODO address multiple usernames
    if g.logged_in and username.lower() is g.user.name.lower():
        user = g.user
    else:
        user = User.by_username(username)

    # User not found
    if user is None:
        return render_template('notfound.html'), 404

    # Redirect the URL if this is not the main username for the user
    if user.name.lower() != username:
        return redirect('/user/' + user.name.lower() + '/', code=302)
    pets = user.pets.all()
    return render_template('profile/main.html', viewed_user=user, pets=pets)
