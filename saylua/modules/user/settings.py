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
        boolean_fields = ['notified_on_pings',
            'ha_disabled', 'autosubscribe_threads', 'autosubscribe_posts']
        save_fields_to_user(request.form, bool_fields=boolean_fields)
        return redirect(url_for('user_settings'))

    # Allows user to change general on/off settings
    return render_template('user/settings/main.html')

@app.route('/settings/details/', methods=['GET', 'POST'])
@login_required
def user_settings_details():
    if request.method == 'POST':
        display_name = request.form['display_name'].strip()
        displayNameValidator = (FieldValidator('display name', display_name)
            .required()
            .min(app.config['MIN_DISPLAY_NAME_LENGTH'])
            .max(app.config['MAX_DISPLAY_NAME_LENGTH']))
        displayNameValidator.flash()

        if displayNameValidator.valid:
            string_fields = ['display_name', 'gender', 'pronouns', 'bio']
            save_fields_to_user(request.form, str_fields=string_fields)
            return redirect(url_for('user_settings_details'))
    return render_template('user/settings/details.html',
        min_display_name_length=app.config['MIN_DISPLAY_NAME_LENGTH'],
        max_display_name_length=app.config['MAX_DISPLAY_NAME_LENGTH'])

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
    return render_template('user/settings/email.html')

@app.route('/settings/password/', methods=['GET', 'POST'])
@login_required
def user_settings_password():
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
