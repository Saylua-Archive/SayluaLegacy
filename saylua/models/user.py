from bcryptmaster import bcrypt

from saylua import db
from saylua.utils import random_token

from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import validates

import datetime


# An exception thrown if an operation would make a user's currency negative
class InvalidCurrencyException(Exception):
    pass


class User(db.Model):
    """The greatest User model of all time.
    """

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)

    active_username = db.Column(db.String(80), unique=True)

    last_username_change = db.Column(db.DateTime(timezone=True), server_default=db.func.now())
    username_objects = db.relationship("Username", back_populates="user")

    last_action = db.Column(db.DateTime(timezone=True), server_default=db.func.now())
    date_joined = db.Column(db.DateTime(timezone=True), server_default=db.func.now())

    # Email, Password
    email = db.Column(db.String(120), unique=True)
    email_confirmed = db.Column(db.Boolean, default=False)
    password_hash = db.Column(db.String(200))

    # Role
    role_name = db.Column(db.String(100), default="user")

    # Human Avatar
    ha_url = db.Column(db.String(100), default="/api/ha/m/")

    # Ban Status
    permabanned = db.Column(db.Boolean, default=False)
    banned_until = db.Column(db.DateTime(timezone=True), server_default=db.func.now())

    # Currency
    star_shards = db.Column(db.Integer, default=0)
    cloud_coins = db.Column(db.Integer, default=0)
    bank_account = db.relationship("BankAccount", uselist=False, back_populates="user")

    # Misc profile stuff
    gender = db.Column(db.String(100), default="")
    pronouns = db.Column(db.String(200), default="")
    bio = db.Column(db.String(1000), default="Hello, world")
    status = db.Column(db.String(15), default="")

    # Settings
    notified_on_pings = db.Column(db.Boolean, default=True)
    autosubscribe_threads = db.Column(db.Boolean, default=True)
    autosubscribe_posts = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return '<User %r>' % self.name

    @hybrid_property
    def name(self):
        return self.active_username

    @name.setter
    def setName(self, name):
        self.active_username = name

    @property
    def usernames(self):
        return [u.name for u in self.username_objects]

    def url(self):
        return "/user/" + self.name.lower() + "/"

    def get_role(self):
        from saylua.models.role import Role
        return (
            db.session.query(Role)
            .filter(Role.name == self.role_name)
            .one_or_none()
        )

    def make_email_confirmation_code(self):
        code = EmailConfirmationCode(self.id, self.email)
        db.session.merge(code)
        db.session.commit()
        return code

    def make_password_reset_code(self):
        code = PasswordResetCode(self.id)
        db.session.merge(code)
        db.session.commit()
        return code

    @validates('email')
    def validate_email(self, key, address):
        return address.lower()

    @classmethod
    def from_username(cls, username):
        return (
            db.session.query(cls)
            .join(Username, cls.id == Username.user_id)
            .filter(Username.name == username.lower())
            .one_or_none()
        )

    @classmethod
    def from_email(cls, email):
        return db.session.query(cls).filter(cls.email == email.lower()).one_or_none()

    @classmethod
    def hash_password(cls, password, salt=None):
        if not salt:
            salt = bcrypt.gensalt()
        return bcrypt.hashpw(password, salt)

    @classmethod
    def check_password(cls, user, password):
        return cls.hash_password(password, user.password_hash) == user.password_hash

    @classmethod
    def update_currency(cls, user_id, cc=0, ss=0):
        user = db.session.query(User).get(user_id)
        user.star_shards += ss
        user.cloud_coins += cc

        # Throw exceptions if the currency amount is invalid
        cls.except_if_currency_invalid(user)
        db.session.add(user)
        db.session.commit()
        return [user.cloud_coins, user.star_shards]

    @classmethod
    def transfer_currency(cls, from_id, to_id, cc=0, ss=0):
        from_user = db.session.query(User).get(from_id)
        to_user = db.session.query(User).get(to_id)
        if cc > from_user.cloud_coins or ss > from_user.star_shards:
            raise InvalidCurrencyException('Insufficient funds!')
        from_user.star_shards -= ss
        from_user.cloud_coins -= cc
        to_user.star_shards += ss
        to_user.cloud_coins += cc

        # Throw exceptions if the currency amount is invalid
        if cc < 0 or ss < 0:
            raise InvalidCurrencyException('Transfers cannot be negative!')
        cls.except_if_currency_invalid(from_user)
        cls.except_if_currency_invalid(to_user)
        db.session.add(from_user)
        db.session.add(to_user)
        db.session.commit()

    @classmethod
    def except_if_currency_invalid(cls, user):
        if user.star_shards < 0 or user.cloud_coins < 0:
            raise InvalidCurrencyException('Currency cannot be negative!')

    def __init__(self, username, email, password_hash, role_name=None, star_shards=None, cloud_coins=None):
        self.active_username = username
        Username.create(username, self)

        self.email = email
        self.password_hash = password_hash

        if role_name:
            self.role_name = role_name

        if star_shards:
            self.star_shards = star_shards

        if cloud_coins:
            self.cloud_coins = cloud_coins

        self.bank_account = BankAccount()


class BankAccount(db.Model):
    """Permanently assigned bank account for the `User` class.

    One to one relationship with `User`.
    """

    __tablename__ = "bank_accounts"

    id = db.Column(db.Integer, db.ForeignKey("users.id"), primary_key=True)
    user = db.relationship("User", back_populates="bank_account")

    star_shards = db.Column(db.Integer, default=0)
    cloud_coins = db.Column(db.Integer, default=0)


class Username(db.Model):
    """Represents the username of a user.

    Multiple names can be tied to one user, but only one of
    them can be active and nested within the user class.

    Many to one relationship with `User`.
    """

    __tablename__ = "usernames"

    # The unique username stored in lowercase.
    name = db.Column(db.String(80), primary_key=True)

    # A record of the name as the user typed it.
    case_name = db.Column(db.String(80))

    # The linked user
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    user = db.relationship("User", back_populates="username_objects")

    # Account for case sensitivity in username uniqueness.
    @classmethod
    def create(cls, name, user):
        return cls(name=name.lower(), case_name=name, user=user)

    # Get username object from username.
    @classmethod
    def get(cls, name):
        return db.session.query(cls).get(name.lower())


class LoginSession(db.Model):
    __tablename__ = "sessions"

    id = db.Column(db.String(256), primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), primary_key=True)
    user = db.relationship("User")

    expires = db.Column(db.DateTime)

    def __init__(self, user_id, expires):
        self.id = random_token(128)
        self.user_id = user_id
        self.expires = expires

    @property
    def active(self):
        return (self.expires > datetime.datetime.now())


class PasswordResetCode(db.Model):
    __tablename__ = "password_reset_codes"

    code = db.Column(db.String(256), primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), primary_key=True)
    user = db.relationship("User")

    # Only set if the code has been used.
    date_used = db.Column(db.DateTime(timezone=True))

    # Use this to determine whether the code is expired.
    date_created = db.Column(db.DateTime(timezone=True), server_default=db.func.now())

    def __init__(self, user_id):
        self.code = random_token()
        self.user_id = user_id

    def expired(self):
        return self.date_created < datetime.datetime.now() - datetime.timedelta(hours=1)

    def invalid(self):
        return self.expired() or self.date_used

    def url(self):
        return '/login/reset/%s/%s' % (self.user_id, self.code)


class EmailConfirmationCode(db.Model):
    __tablename__ = "email_confirmation_codes"

    code = db.Column(db.String(256), primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), primary_key=True)
    user = db.relationship("User")

    # Record the email address the user had when making the confirmation request.
    email = db.Column(db.String(120))

    # Use this to determine whether the code is expired.
    date_created = db.Column(db.DateTime(timezone=True), server_default=db.func.now())

    def __init__(self, user_id, email):
        self.code = random_token()
        self.user_id = user_id
        self.email = email

    def url(self):
        return '/register/email/?id=%s&code=%s' % (self.user_id, self.code)

    def expired(self):
        return self.date_created < datetime.datetime.now() - datetime.timedelta(days=1)

    def invalid(self):
        return self.expired() or self.email != self.user.email


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

    date_created = db.Column(db.DateTime(timezone=True), server_default=db.func.now())

    def __init__(self, sender_id):
        self.code = random_token()
        self.sender_id = sender_id

    def url(self):
        return '/register/?invite_code=' + self.code
