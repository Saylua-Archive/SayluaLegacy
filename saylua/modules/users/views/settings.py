from saylua import app, db
from saylua.models.user import User, Username
from saylua.wrappers import login_required

from saylua.utils.email import send_confirmation_email

from flask import render_template, redirect, g, url_for, flash, request

from ..forms.settings import (GeneralSettingsForm, DetailsForm, UsernameForm,
    EmailForm, PasswordForm)

import datetime


# User Settings
@login_required
def user_settings():
    form = GeneralSettingsForm(request.form, obj=g.user)
    if form.validate_on_submit():
        form.populate_obj(g.user)
        db.session.commit()
        flash("Your settings have been saved.")

    # Allows user to change general on/off settings
    return render_template("settings/main.html", form=form)


@login_required
def user_settings_details():
    form = DetailsForm(request.form, obj=g.user)
    if form.validate_on_submit():
        form.populate_obj(g.user)
        db.session.commit()
        flash("Your user details have been saved.")
    return render_template("settings/details.html", form=form)


@login_required
def user_settings_username():
    form = UsernameForm(request.form, obj={"username": g.user.name})
    form.setUser(g.user)

    cutoff_time = datetime.datetime.now() - datetime.timedelta(days=1)
    can_change = g.user.last_username_change < cutoff_time
    if form.validate_on_submit():
        username = form.username.data
        if username.lower() in g.user.usernames:
            # If the user is changing to a name they already own, change case
            g.user.name = username
            g.user.last_username_change = datetime.datetime.now()
            username_obj = Username.get(username)
            username_obj.case_name = username
            db.session.commit()
            flash("Your username has been changed to " + username)
            return redirect(url_for("users.settings_username"))
        else:
            # If the username does not exist things are fine as well.
            if not can_change:
                flash("You've already changed your username within the past 24 hours.", "error")
                return redirect(url_for("users.settings_username"))
            max_usernames = app.config['MAX_USERNAMES']
            if len(g.user.usernames) >= max_usernames:
                # User cannot exceed maximum number of usernames.
                flash("""You can't have more than %d usernames.
                    Release some old usernames to change your name.""" % max_usernames,
                    "error")
                return render_template('user/settings/username.html')
            g.user.name = username
            g.user.last_username_change = datetime.datetime.now()
            new_username = Username.create(username, g.user)
            db.session.commit()
            flash("Your username has been changed to " + new_username.name)
            return redirect(url_for("users.settings_username"))

    return render_template("settings/username.html", form=form)


@login_required
def user_settings_username_release():
    username = request.form.get("username")
    if not username or username not in g.user.usernames:
        flash("You are trying to release an invalid username.", "error")
    elif username == g.user.name.lower():
        flash("You can't release the username you are currently using.", "error")
    else:
        Username.query.filter_by(name=username).delete()
        db.session.commit()
        flash("You've successfully released the username " + username)
    return redirect(url_for("users.settings_username"))


@login_required
def user_settings_email():
    form = EmailForm(request.form, obj=g.user)
    form.setUser(g.user)
    if form.validate_on_submit():
        g.user.email = form.email.data
        g.user.email_confirmed = False
        db.session.commit()
        flash("Your email address has been changed! A confirmation has been sent to your new email.")

        # Success! Send confirmation email.
        send_confirmation_email(g.user)

    return render_template("settings/email.html", form=form)


@login_required
def user_settings_password():
    form = PasswordForm(request.form)
    form.setUser(g.user)
    if form.validate_on_submit():
        password = form.new_password.data
        g.user.password_hash = User.hash_password(password)
        db.session.commit()
        flash("Your password has been changed.")
        return redirect(url_for("users.settings_password"))

    return render_template("settings/password.html", form=form)
