from flask import flash

from wtforms import validators
from saylua.models.user import User

def flash_errors(form):
    for field, errors in form.errors.items():
        for error in errors:
            flash(error, 'error')

# Used mainly for login, but also for other places.
class UserCheck:
    def __init__(self, user=None):
        self.user = user

    def UsernameExists(self, form, field):
        self.user = User.by_username(field.data)
        if not self.user:
            raise validators.StopValidation("We can't find a user with that name.")

    def PasswordValid(self, form, field):
        if not self.user:
            return
        if not User.check_password(self.user, field.data):
            raise validators.StopValidation("Your password is incorrect.")
