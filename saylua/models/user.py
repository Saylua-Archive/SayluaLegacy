from google.appengine.ext import ndb

class User(ndb.Model):
    username = ndb.StringProperty(indexed=True)
    display_name = ndb.StringProperty()
    phash = ndb.StringProperty()
    email = ndb.StringProperty(indexed=True)
    email_verified = ndb.BooleanProperty()
    star_shards = ndb.IntegerProperty()
    opal_hearts = ndb.IntegerProperty()

class LoginSession(ndb.Model):
    username = ndb.StringProperty(indexed=True)
    session_key = ndb.StringProperty()
    expires = ndb.DateTimeProperty()
