from saylua import app, login_required
from flask import (render_template, redirect, g,
                   url_for, flash, session, abort, request)
import datetime

from saylua.utils.form import flash_errors
from saylua.models.user import User
from forms.settings import DetailsForm, UsernameForm, EmailForm, PasswordForm

# User Settings
@app.route('/settings/', methods=['GET', 'POST'])
@login_required
def user_settings():
    if request.method == 'POST':
        boolean_fields = ['notified_on_pings', 'ha_disabled',
            'autosubscribe_threads', 'autosubscribe_posts']
        save_fields_to_user(request.form, bool_fields=boolean_fields)

    # Allows user to change general on/off settings
    return render_template('user/settings/main.html')

@app.route('/settings/details/', methods=['GET', 'POST'])
@login_required
def user_settings_details():
    form = DetailsForm(request.form)
    if request.method == 'POST' and form.validate():
        form.populate_obj(g.user)
        g.user.put()
        flash('Your user details have successfully been saved. ')
    flash_errors(form)
    return render_template('user/settings/details.html', form=form)

@app.route('/settings/css/', methods=['GET', 'POST'])
@login_required
def user_settings_css():
    if request.method == 'POST':
        string_fields = ['css']
        save_fields_to_user(request.form, str_fields=string_fields)
    return render_template("user/settings/css.html")

@app.route('/settings/username/', methods=['GET', 'POST'])
@login_required
def user_settings_username():
    form = UsernameForm(request.form)
    form.setUser(g.user)

    # Make sure if a user tries to submit a blank form it does not autofill to
    # their current name.
    if request.method != 'POST':
        form.username.data = form.username.data or g.user.display_name

    cutoff_time = datetime.datetime.now() - datetime.timedelta(days=1)
    can_change = g.user.last_username_change < cutoff_time
    if request.method == 'POST' and form.validate():
        if not can_change:
            flash('You\'ve already changed your username once within the past 24 hours!', 'error')
            return redirect(url_for('user_settings_username'))

        username = form.username.data
        user_key = User.key_by_username(username)
        if username.lower() in g.user.usernames:
            # If the user is changing to a name they already own, change case
            g.user.display_name = username
            g.user.usernames.remove(username.lower())
            g.user.usernames.append(username.lower())
            g.user.last_username_change = datetime.datetime.now()
            g.user.put()
            flash('You have successfully updated your username to ' + username)
            return redirect(url_for('user_settings_username'))
        else:
            # If the username does not exist things are fine as well.
            max_usernames = app.config['MAX_USERNAMES']
            if len(g.user.usernames) >= max_usernames:
                # User cannot exceed maximum number of usernames.
                flash('You cannot have more than %d usernames. Release some old usernames to change your name.' % max_usernames,
                    'error')
                return render_template('user/settings/username.html')
            g.user.display_name = username
            g.user.usernames.append(username.lower())
            g.user.last_username_change = datetime.datetime.now()
            g.user.put()
            flash('You have successfully changed your username to ' + username)
            return redirect(url_for('user_settings_username'))
    flash_errors(form)

    return render_template('user/settings/username.html', form=form)


@app.route('/settings/username/release/', methods=['POST'])
@login_required
def user_settings_username_release():
    username = request.form.get('username')
    if not username or not username in g.user.usernames:
        flash('You are trying to release an invalid username!', 'error')
    elif username == g.user.display_name.lower():
        flash('You cannot release the username you are currently using!', 'error')
    else:
        g.user.usernames.remove(username)
        g.user.put()
        flash('You have successfully released the username ' + username)
    return redirect(url_for('user_settings_username'))

@app.route('/settings/email/', methods=['GET', 'POST'])
@login_required
def user_settings_email():
    form = EmailForm(request.form)
    form.setUser(g.user)
    if request.method == 'POST' and form.validate():
        g.user.email = form.email.data
        g.user.email_verified = False
        g.user.put()
        flash('Your email has successfully been changed! ')

        # TODO Send new validation email here.
    flash_errors(form)

    return render_template('user/settings/email.html', form=form)

@app.route('/settings/password/', methods=['GET', 'POST'])
@login_required
def user_settings_password():
    form = PasswordForm(request.form)
    form.setUser(g.user)
    if request.method == 'POST' and form.validate():
        password = form.new_password.data

        g.user.phash = User.hash_password(password)
        g.user.put()
        flash('Your password has successfully been changed! ')

        return redirect(url_for('user_settings_password'))
    flash_errors(form)

    return render_template('user/settings/password.html', form=form)

def save_fields_to_user(request, bool_fields=[], str_fields=[], int_fields=[]):
    for field in bool_fields:
        setattr(g.user, field, bool(request[field]))

    for field in int_fields:
        setattr(g.user, field, int(request[field]))

    for field in str_fields:
        value = ''
        if request[field]:
            value = request[field]
        setattr(g.user, field, value.strip())

    # Commit changes
    g.user.put()
    flash('Your settings have been saved! ')
    return
