from google.appengine.ext import ndb
from bcryptmaster import bcrypt

class User(ndb.Model):
    usernames = ndb.StringProperty(indexed=True, repeated=True)
    display_name = ndb.StringProperty(indexed=True)
    status = ndb.StringProperty(default='')
    phash = ndb.StringProperty()
    email = ndb.StringProperty(indexed=True)
    email_verified = ndb.BooleanProperty(default=False)
    date_joined = ndb.DateTimeProperty(auto_now_add=True)
    last_action = ndb.DateTimeProperty(auto_now_add=True)

    # Human Avatar
    ha_url = ndb.StringProperty(default='/api/ha/m/')

    # Ban Status
    permabanned = ndb.BooleanProperty(default=False)
    banned_until = ndb.DateTimeProperty(auto_now_add=True)

    # Currency
    star_shards = ndb.IntegerProperty(default=0)
    cloud_coins = ndb.IntegerProperty(default=0)

    # Settings
    notified_on_pings = ndb.BooleanProperty(default=True)
    ha_disabled = ndb.BooleanProperty(default=False)
    autosubscribe_threads = ndb.BooleanProperty(default=True)
    autosubscribe_posts = ndb.BooleanProperty(default=False)

    # Misc profile stuff
    css = ndb.StringProperty(default='')
    gender = ndb.StringProperty(default='')
    pronouns = ndb.StringProperty(default='')
    bio = ndb.StringProperty(default='')

    @classmethod
    def by_username(cls, username):
        return cls.query(cls.usernames==username).get()

    @classmethod
    def key_by_username(cls, username):
        return cls.query(cls.usernames==username).get(keys_only=True)

    @classmethod
    def hash_password(cls, password, salt=None):
        if not salt:
            salt = bcrypt.gensalt()
        return bcrypt.hashpw(password, salt)

    @classmethod
    def check_password(cls, user, password):
        return cls.hash_password(password, user.phash) == user.phash

class LoginSession(ndb.Model):
    user_key = ndb.StringProperty(indexed=True)
    expires = ndb.DateTimeProperty()
