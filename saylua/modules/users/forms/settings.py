from saylua import app

from flask_wtf import FlaskForm
from wtforms import BooleanField
from saylua.utils.form import sl_validators, UserCheck
from saylua.utils.form.fields import SlField, SlTextAreaField, SlPasswordField


class GeneralSettingsForm(FlaskForm):
    notified_on_pings = BooleanField('Receive notifications for pings?')
    autosubscribe_threads = BooleanField('Autosubscribe to your own threads?')
    autosubscribe_posts = BooleanField('Autosubscribe to threads you post on?')


class DetailsForm(FlaskForm):
    status = SlField('Status', [sl_validators.Max(app.config['MAX_USER_STATUS_LENGTH'])])
    gender = SlField('Gender')
    pronouns = SlField('Pronouns')
    bio = SlTextAreaField('About Me')


class UsernameForm(FlaskForm):
    IsNot = sl_validators.IsNot('',
            message='The username you entered is the same as your current username.')
    UsernameUnique = sl_validators.UsernameUnique()

    username = SlField('New Username', [
        sl_validators.Required(),
        sl_validators.Min(app.config['MIN_USERNAME_LENGTH']),
        sl_validators.Max(app.config['MAX_USERNAME_LENGTH']),
        sl_validators.Username(),
        IsNot,
        UsernameUnique])

    def setUser(self, user):
        self.IsNot.pattern = user.name
        self.UsernameUnique.whitelist = user.usernames


class EmailForm(FlaskForm):
    password_check = UserCheck()

    IsNot = sl_validators.IsNot('',
            message='The email you entered is the same as your old email.')

    email = SlField('Email Address', [
        sl_validators.Required(),
        sl_validators.Email(),
        IsNot,
        sl_validators.EmailUnique()])

    password = SlPasswordField('Password', [
        sl_validators.Required(),
        password_check.PasswordValid])

    def setUser(self, user):
        self.password_check.user = user
        self.IsNot.pattern = user.email


class PasswordForm(FlaskForm):
    password_check = UserCheck()

    old_password = SlPasswordField('Old Password', [
        sl_validators.Required(),
        password_check.PasswordValid])

    new_password = SlPasswordField('New Password', [
        sl_validators.Required(),
        sl_validators.Min(app.config['MIN_PASSWORD_LENGTH']),
        sl_validators.Max(app.config['MAX_PASSWORD_LENGTH'])
    ])
    confirm_password = SlPasswordField('Confirm Password', [
        sl_validators.EqualTo('new_password', message='Passwords must match.')
    ])

    def setUser(self, user):
        self.password_check.user = user
