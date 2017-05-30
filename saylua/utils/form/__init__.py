from wtforms import validators

from saylua import app, db
from saylua.modules.users.models.db import User, InviteCode

import re


# Used mainly for login, but also for other places.
# This is sort of hackish. Basically, it's used to make sure we don't query for
# the user object more than necessary during form validation.
class UserCheck:
    def __init__(self, user=None):
        self.user = user

    def UsernameOrEmailExists(self, form, field):
        pattern = re.compile(app.config['EMAIL_REGEX'])

        # If this is an email.
        if pattern.match(field.data):
            self.user = User.from_email(field.data)
            if not self.user:
                raise validators.StopValidation(
                    "We can't find a user with the email %s." % field.data)
        else:
            self.user = User.by_username(field.data)
            if not self.user:
                raise validators.StopValidation(
                    "We can't find a user with the name %s." % field.data)

    def UsernameExists(self, form, field):
        self.user = User.by_username(field.data)
        if not self.user:
            raise validators.StopValidation(
                "We can't find a user with the name %s." % field.data)

    def PasswordValid(self, form, field):
        if not self.user:
            return
        if not User.check_password(self.user, field.data):
            raise validators.StopValidation("Your password is incorrect.")

    def InviteCodeValid(self, form, field):
        self.invite_code = db.session.query(InviteCode).get(field.data)
        if not self.invite_code or self.invite_code.disabled:
            raise validators.StopValidation(
                "Sorry, the invite code you entered is invalid.")
        elif self.invite_code.recipient_id:
            raise validators.StopValidation(
                "Sorry, the invite code you entered has already been claimed.")
