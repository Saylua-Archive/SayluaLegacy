from saylua import app, login_required
from flask import (render_template, redirect, g,
                   url_for, flash, session, abort, request)
import datetime

from saylua.models.user import User
from saylua.utils.validation import FieldValidator

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
    if request.method == 'POST':
        status = request.form['status']
        statusValidator = (FieldValidator('status', status)
            .max(app.config['MAX_USER_STATUS_LENGTH']))
        statusValidator.flash()

        if statusValidator.valid:
            string_fields = ['status', 'gender', 'pronouns', 'bio']
            save_fields_to_user(request.form, str_fields=string_fields)
    return render_template('user/settings/details.html')

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
    if request.method == 'POST':
        cutoff_time = datetime.datetime.now() - datetime.timedelta(days=1)
        if g.user.last_username_change > cutoff_time:
            flash('You\'ve already changed your username once within the past 24 hours!')
            return redirect(url_for('user_settings_username'))

        username = request.form.get('username')
        if username == g.user.display_name:
            # In this case, the user did not make any changes to their name.
            flash('The username you entered is the same as your old username.')
            return redirect(url_for('user_settings_username'))
        usernameValidator = (FieldValidator('username', username)
            .required()
            .min(app.config['MIN_USERNAME_LENGTH'])
            .max(app.config['MAX_USERNAME_LENGTH'])
            .matches_regex('^[A-Za-z0-9+~._-]+$', error='Usernames may only contain letters, numbers, and these characters: +~._-'))
        usernameValidator.flash()

        if usernameValidator.valid:
            user_key = User.key_by_username(username)
            if user_key == g.user.key:
                # If the user is changing to a name they alrady own, they can change
                g.user.display_name = username
                g.user.usernames.remove(username.lower())
                g.user.usernames.append(username.lower())
                g.user.last_username_change = datetime.datetime.now()
                g.user.put()
                flash('You have successfully updated your username to ' + username)
                return redirect(url_for('user_settings_username'))
            elif not user_key:
                # If the username does not exist things are fine as well.
                max_usernames = app.config['MAX_USERNAMES']
                if len(g.user.usernames) >= max_usernames:
                    # User cannot exceed maximum number of usernames.
                    flash('You cannot have more than ' + str(max_usernames) + ' usernames. Release some old usernames to change your name. ', 'error')
                    return render_template('user/settings/username.html')
                g.user.display_name = username
                g.user.usernames.append(username.lower())
                g.user.last_username_change = datetime.datetime.now()
                g.user.put()
                flash('You have successfully changed your username to ' + username)
                return redirect(url_for('user_settings_username'))
            else:
                flash('The username you are trying to change to is already taken!', 'error')

    return render_template('user/settings/username.html')


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
    if request.method == 'POST':
        email = request.form.get('email')

        if g.user.email == email:
            flash('The email you entered is the same as your old email. ')
            return redirect(url_for('user_settings_email'))

        emailValidator = (FieldValidator('email', email)
            .required()
            .min(5, error='You must enter a valid email address.'))

        emailValidator.flash()
        if emailValidator.valid:
            g.user.email = email
            g.user.email_verified = False
            g.user.put()
            flash('Your email has successfully been changed! ')

            # TODO Send new validation email here.


    return render_template('user/settings/email.html')

@app.route('/settings/password/', methods=['GET', 'POST'])
@login_required
def user_settings_password():
    if request.method == 'POST':
        old_password = request.form.get('old_password')
        password = request.form.get('new_password')
        password2 = request.form.get('new_password2')
        if not User.check_password(g.user, old_password):
            flash('The old password you entered is incorrect. ', 'error')
            return redirect(url_for('user_settings_password'))

        passwordValidator = (FieldValidator('new password', password)
            .required()
            .min(app.config['MIN_PASSWORD_LENGTH'])
            .max(app.config['MAX_PASSWORD_LENGTH'])
            .matches(password2, error='New passwords must match.'))
        passwordValidator.flash()
        if passwordValidator.valid:
            g.user.phash = User.hash_password(password)
            g.user.put()
            flash('Your password has successfully been changed! ')

            return redirect(url_for('user_settings_password'))

    return render_template('user/settings/password.html')

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
