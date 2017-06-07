from saylua import db
from saylua.utils import random_token

import datetime


class PasswordResetCode(db.Model):
    __tablename__ = "password_reset_codes"

    code = db.Column(db.String(256), primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), primary_key=True)
    user = db.relationship("User")

    used = db.Column(db.Boolean, default=False)

    # Use this to determine whether the code is expired.
    date_created = db.Column(db.DateTime, server_default=db.func.now())

    def __init__(self, user_id):
        self.code = random_token()
        self.user_id = user_id

    def expired(self):
        return self.date_created < (datetime.datetime.now() - datetime.timedelta(hours=1))

    def invalid(self):
        return self.expired() or self.used

    def url(self):
        return '/login/reset/%s/%s/' % (self.user_id, self.code)


class EmailConfirmationCode(db.Model):
    __tablename__ = "email_confirmation_codes"

    code = db.Column(db.String(256), primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), primary_key=True)
    user = db.relationship("User")

    used = db.Column(db.Boolean, default=False)

    # Record the email address the user had when making the confirmation request.
    email = db.Column(db.String(120))

    # Use this to determine whether the code is expired.
    date_created = db.Column(db.DateTime, server_default=db.func.now())

    def __init__(self, user_id, email):
        self.code = random_token()
        self.user_id = user_id
        self.email = email

    def url(self):
        return '/register/email/?id=%s&code=%s' % (self.user_id, self.code)

    def expired(self):
        return self.date_created < (datetime.datetime.now() - datetime.timedelta(days=1))

    def invalid(self):
        return self.expired() or self.used or self.email != self.user.email


class InviteCode(db.Model):
    __tablename__ = "invite_codes"

    code = db.Column(db.String(256), primary_key=True)

    # An invite code is considered claimed if a recipient user exists.
    recipient_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    recipient = db.relationship("User", foreign_keys=[recipient_id])

    # The person who originally created the invite code.
    sender_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    sender = db.relationship("User", foreign_keys=[sender_id])

    disabled = db.Column(db.Integer, default=False)

    date_created = db.Column(db.DateTime, server_default=db.func.now())

    def __init__(self, sender_id):
        self.code = random_token()
        self.sender_id = sender_id

    def url(self):
        return '/register/?invite_code=' + self.code
