from google.appengine.ext import ndb

class User(ndb.Model):
    username = ndb.StringProperty(indexed=True)
    display_name = ndb.StringProperty()
    phash = ndb.StringProperty()
    email = ndb.StringProperty(indexed=True)
    email_verified = ndb.BooleanProperty(default=False)
    date_joined = ndb.DateTimeProperty(auto_now_add=True)
    last_action = ndb.DateTimeProperty(auto_now_add=True)

    # Currency
    star_shards = ndb.IntegerProperty(default=0)
    opal_hearts = ndb.IntegerProperty(default=0)

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


class LoginSession(ndb.Model):
    user_key = ndb.StringProperty(indexed=True)
    session_key = ndb.StringProperty()
    expires = ndb.DateTimeProperty()
