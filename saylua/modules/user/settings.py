from saylua import app, login_required
from flask import (render_template, redirect, g,
                   url_for, flash, session, abort, request)
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
        return redirect(url_for('user_settings'))

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
            return redirect(url_for('user_settings_details'))
    return render_template('user/settings/details.html',
        max_status_length=app.config['MAX_USER_STATUS_LENGTH'])

@app.route('/settings/css/', methods=['GET', 'POST'])
@login_required
def user_settings_css():
    if request.method == 'POST':
        string_fields = ['css']
        save_fields_to_user(request.form, str_fields=string_fields)
        return redirect(url_for('user_settings_css'))
    return render_template("user/settings/css.html")

@app.route('/settings/email/', methods=['GET', 'POST'])
@login_required
def user_settings_email():
    if request.method == 'POST' and 'email' in request.form:
        email = request.form['email']

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

            return redirect(url_for('user_settings_email'))

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
