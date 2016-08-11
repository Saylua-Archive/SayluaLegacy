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
        user = User.query(User.username == username).get()

    if user == None:
        return render_template('user/notfound.html')

    return render_template('user/profile.html', viewed_user=user)

# Users Online
@app.route('/online/')
def users_online():
    return render_template('user/online.html')

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
        if len(display_name) < 2:
            flash('Your display name must be at least two characters long!',
                'error')
        elif len(display_name) > 25:
            flash('Your display name cannot be more than 25 characters long!',
                'error')
        else:
            string_fields = ['display_name', 'gender', 'pronouns', 'bio']
            save_fields_to_user(request.form, str_fields=string_fields)
            return redirect(url_for('user_settings_details'))
    return render_template("user/settings/details.html")

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
