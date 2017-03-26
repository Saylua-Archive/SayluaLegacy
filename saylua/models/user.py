from bcryptmaster import bcrypt
from uuid import uuid4
import datetime

from sqlalchemy.exc import IntegrityError

from saylua import db


# An exception thrown if an operation would make a user's currency negative
class InvalidCurrencyException(Exception):
    pass


class User(db.Model):
    """The greatest User model of all time.
    """

    __tablename__ = "users"

    __table_args__ = (
        db.ForeignKeyConstraint(
            ["id", "active_username"],
            ["usernames.user_id", "usernames.name"],
            use_alter=True,
            name="fk_user_usernames"
        ),
        db.ForeignKeyConstraint(
            ["active_username"],
            ["usernames.name"],
            use_alter=True,
            name="fk_user_active_username"
        )
    )

    id = db.Column(db.Integer, primary_key=True)

    active_username = db.Column(db.String(80), db.ForeignKey("usernames.name"))
    usernames = db.relationship("Username", foreign_keys="Username.user_id", back_populates="user")
    last_username_change = db.Column(db.DateTime(timezone=True), server_default=db.func.now())

    last_action = db.Column(db.DateTime(timezone=True), server_default=db.func.now())
    date_joined = db.Column(db.DateTime(timezone=True), server_default=db.func.now())

    # Email, Password
    email = db.Column(db.String(120), unique=True)
    email_verified = db.Column(db.Boolean, default=False)
    phash = db.Column(db.String(200))

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

    @property
    def name(self):
        return self.active_username

    def url(self):
        return "/user/" + self.name.lower() + "/"

    def get_role(self):
        from saylua.models.role import Role
        return (
            db.session.query(Role)
            .filter(Role.name == self.role_name)
            .one_or_none()
        )

    @classmethod
    def from_username(cls, username):
        return (
            db.session.query(cls)
            .join(Username, cls.username)
            .filter(db.func.lower(Username.username) == username.lower())
            .one_or_none()
        )

    @classmethod
    def hash_password(cls, password, salt=None):
        if not salt:
            salt = bcrypt.gensalt()
        return bcrypt.hashpw(password, salt)

    @classmethod
    def check_password(cls, user, password):
        return cls.hash_password(password, user.phash) == user.phash

    @classmethod
    def update_currency(cls, user_id, cc=0, ss=0):
        return

    @classmethod
    def transfer_currency(cls, from_id, to_id, cc=0, ss=0):
        #     from_user, to_user = ndb.get_multi([from_key, to_key])
        #     from_user.star_shards -= ss
        #     from_user.cloud_coins -= cc
        #     to_user.star_shards += ss
        #     to_user.cloud_coins += cc

        #     # Throw exceptions if the currency amount is invalid
        #     cls.except_if_currency_invalid(from_user)
        #     cls.except_if_currency_invalid(to_user)

        #     ndb.put_multi([from_user, to_user])
        return

    # @classmethod
     # def update_currency(cls, user_id, cc=0, ss=0):
     #     user = user_id.get()
     #     user.star_shards += ss
     #     user.cloud_coins += cc

     #     # Throw exceptions if the currency amount is invalid
     #     cls.except_if_currency_invalid(user)
     #     user.put()
     #     return [user.cloud_coins, user.star_shards]

     # @classmethod
     # def except_if_currency_invalid(cls, user):
     #     if user.star_shards < 0 or user.cloud_coins < 0:
     #         raise InvalidCurrencyException('Currency cannot be negative!')

    def __init__(self, username, email, phash, role_name=None, star_shards=None, cloud_coins=None):
        self.active_username = Username(username)
        self.email = email
        self.phash = phash

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

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    user = db.relationship("User", back_populates="bank_account")
    bank_ss = db.Column(db.Integer, default=0)
    bank_cc = db.Column(db.Integer, default=0)


class Username(db.Model):
    """Represents the username of a user.

    Multiple names can be tied to one user, but only one of
    them can be active and nested within the user class.

    Many to one relationship with `User`.
    """

    __tablename__ = "usernames"

    # The unique username
    name = db.Column(db.String(80), primary_key=True)

    # The linked user
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    user = db.relationship("User", foreign_keys=[user_id], back_populates="usernames")

    # Account for case sensitivity in username uniqueness.
    def __init__(self, name):
        if Username.exists(name):
            raise IntegrityError("Attempted to create username which already exists.")
        self.name = name

    # Check to see if a given username is already taken or not.
    @classmethod
    def exists(cls, name):
        return (
            db.session.query(cls)
            .filter(db.func.lower(cls.name) == name.lower())
            .one_or_none()
        )


class LoginSession(db.Model):
    """User login session.
    """

    __tablename__ = "sessions"

    id = db.Column(db.String(256), primary_key=True)
    user_id = db.Column(db.Integer)
    expires = db.Column(db.DateTime)

    def __init__(self, user_id, expires):
        self.id = str(uuid4())
        self.user_id = user_id
        self.expires = expires

    @property
    def active(self):
        return (self.expires > datetime.datetime.now())

    def get_user(self):
        return (
            db.session.query(User)
            .filter(User.id == self.user_id)
            .one_or_none()
        )
