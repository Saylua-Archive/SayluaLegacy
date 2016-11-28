from saylua import app

from wtforms import Form, RadioField
from saylua.utils.form import sl_validators, UserCheck
from saylua.utils.form.fields import SlField, SlTextAreaField, SlPasswordField


class GeneralSettingsForm(Form):
    notified_on_pings = RadioField('Receive notifications for pings?',
        choices=[('True', 'Yes'), ('False', 'No')])
    ha_disabled = RadioField('Disable Human Avatars?',
        choices=[('True', 'Yes'), ('False', 'No')])
    autosubscribe_threads = RadioField('Autosubscribe to your own threads?',
        choices=[('True', 'Yes'), ('False', 'No')])
    autosubscribe_posts = RadioField('Autosubscribe to threads you post on?',
        choices=[('True', 'Yes'), ('False', 'No')])

    def populate_obj(self, obj):
        obj.notified_on_pings = self.notified_on_pings.data == 'True'
        obj.ha_disabled = self.ha_disabled == 'True'
        obj.autosubscribe_threads = self.autosubscribe_threads.data == 'True'
        obj.autosubscribe_posts = self.autosubscribe_posts.data == 'True'


class DetailsForm(Form):
    status = SlField('Status', [sl_validators.Max(app.config['MAX_USER_STATUS_LENGTH'])])
    gender = SlField('Gender')
    pronouns = SlField('Pronouns')
    bio = SlTextAreaField('About Me')


class UsernameForm(Form):
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
        self.IsNot.pattern = user.display_name
        self.UsernameUnique.whitelist = user.usernames


class EmailForm(Form):
    IsNot = sl_validators.IsNot('',
            message='The email you entered is the same as your old email.')

    email = SlField('Email Address', [
        sl_validators.Required(),
        sl_validators.Email(),
        IsNot])

    def setUser(self, user):
        self.IsNot.pattern = user.email


class PasswordForm(Form):
    password_check = UserCheck()

    old_password = SlPasswordField('Old Password', [
        sl_validators.Required(),
        password_check.PasswordValid])

    new_password = SlPasswordField('New Password', [
        sl_validators.Required(),
        sl_validators.Min(app.config['MIN_PASSWORD_LENGTH']),
        sl_validators.Max(app.config['MAX_PASSWORD_LENGTH']),
        sl_validators.EqualTo('confirm_password', message='Passwords must match.')
    ])
    confirm_password = SlPasswordField('Confirm Password')

    def setUser(self, user):
        self.password_check.user = user
