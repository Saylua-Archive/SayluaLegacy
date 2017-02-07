from google.appengine.ext import ndb
from bcryptmaster import bcrypt
from saylua.models.role import Role

from saylua import db


class _User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    display_name = db.Column(db.String(80), unique=True)
    email = db.Column(db.String(120), unique=True)
    phash = db.Column(db.String(200))
    role = db.Column(db.String(100), default="user")
    ha_url = db.Column(db.String(100), default="/api/ha/m/")
    permabanned = Column(Boolean, default=False)
    star_shards = db.Column(db.Integer, default=0)
    cloud_coins = db.Column(db.Integer, default=0)
    bank_cc = db.Column(db.Integer, default=0)
    bank_ss = db.Column(db.Integer, default=0)

    def __repr__(self):
        return '<User %r>' % self.display_name


class User(ndb.Model):
    # An exception thrown if an operation would make a user's currency negative
    class InvalidCurrencyException(Exception):
        pass

    # A user can have multiple unique usernames. Usernames are NOT case sensitive.
    usernames = ndb.StringProperty(repeated=True)

    # A user's display name must be one of their usernames. Display names are case sensitive.
    display_name = ndb.StringProperty()

    last_username_change = ndb.DateTimeProperty(auto_now_add=True)

    status = ndb.StringProperty(default='')
    phash = ndb.StringProperty(indexed=False)
    email = ndb.StringProperty()
    email_verified = ndb.BooleanProperty(default=False)
    date_joined = ndb.DateTimeProperty(auto_now_add=True)
    last_action = ndb.DateTimeProperty(auto_now_add=True)

    # Human Avatar
    ha_url = ndb.StringProperty(default='/api/ha/m/', indexed=False)

    # Ban Status
    permabanned = ndb.BooleanProperty(default=False)
    banned_until = ndb.DateTimeProperty(auto_now_add=True)

    # Privilege Role
    role_id = ndb.StringProperty(default='user')

    # Currency
    star_shards = ndb.IntegerProperty(default=0)
    cloud_coins = ndb.IntegerProperty(default=0)
    bank_cc = ndb.IntegerProperty(default=0)
    bank_ss = ndb.IntegerProperty(default=0)

    # Settings
    notified_on_pings = ndb.BooleanProperty(default=True)
    ha_disabled = ndb.BooleanProperty(default=False)
    autosubscribe_threads = ndb.BooleanProperty(default=True)
    autosubscribe_posts = ndb.BooleanProperty(default=False)

    # Misc profile stuff
    css = ndb.StringProperty(default='', indexed=False)
    gender = ndb.StringProperty(default='', indexed=False)
    pronouns = ndb.StringProperty(default='', indexed=False)
    bio = ndb.StringProperty(default='', indexed=False)

    def get_role(self):
        return Role.get_by_id(self.role_id)

    @classmethod
    def by_username(cls, username):
        return cls.query(cls.usernames == username.lower()).get()

    @classmethod
    def key_by_username(cls, username):
        return cls.query(cls.usernames == username.lower()).get(keys_only=True)

    @classmethod
    def hash_password(cls, password, salt=None):
        if not salt:
            salt = bcrypt.gensalt()
        return bcrypt.hashpw(password, salt)

    @classmethod
    def check_password(cls, user, password):
        return cls.hash_password(password, user.phash) == user.phash

    @classmethod
    @ndb.transactional(xg=True)
    def transfer_currency(cls, from_key, to_key, cc=0, ss=0):
        from_user, to_user = ndb.get_multi([from_key, to_key])
        from_user.star_shards -= ss
        from_user.cloud_coins -= cc

        to_user.star_shards += ss
        to_user.cloud_coins += cc

        # Throw exceptions if the currency amount is invalid
        cls.except_if_currency_invalid(from_user)
        cls.except_if_currency_invalid(to_user)

        ndb.put_multi([from_user, to_user])

    @classmethod
    @ndb.transactional
    def update_currency(cls, user_key, cc=0, ss=0):
        user = user_key.get()
        user.star_shards += ss
        user.cloud_coins += cc

        # Throw exceptions if the currency amount is invalid
        cls.except_if_currency_invalid(user)
        user.put()
        return [user.cloud_coins, user.star_shards]

    @classmethod
    def except_if_currency_invalid(cls, user):
        if user.star_shards < 0 or user.cloud_coins < 0:
            raise cls.InvalidCurrencyException('Currency cannot be negative!')


class LoginSession(ndb.Model):
    user_key = ndb.StringProperty()
    expires = ndb.DateTimeProperty(indexed=False)

class _LoginSession(ndb.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    expires = db.Column(db.DateTime)
