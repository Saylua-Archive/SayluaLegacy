from flask import flash

from wtforms import validators

from saylua import app
from saylua.models.user import User

import re


def flash_errors(form):
    for field, errors in form.errors.items():
        for error in errors:
            flash(error, 'error')


# Used mainly for login, but also for other places.
class UserCheck:
    def __init__(self, user=None):
        self.user = user

    def UsernameOrEmailExists(self, form, field):
        pattern = re.compile(app.config['EMAIL_REGEX'])

        # If this is an email.
        if pattern.match(field.data):
            self.user = User.from_email(field.data)
        else:
            self.user = User.from_username(field.data)

        if not self.user:
            raise validators.StopValidation(
                "We can't find a user with the name %s." % field.data)

    def UsernameExists(self, form, field):
        self.user = User.from_username(field.data)
        if not self.user:
            raise validators.StopValidation(
                "We can't find a user with the name %s." % field.data)

    def PasswordValid(self, form, field):
        if not self.user:
            return
        if not User.check_password(self.user, field.data):
            raise validators.StopValidation("Your password is incorrect.")
