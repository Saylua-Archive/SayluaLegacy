from google.appengine.ext import ndb

class Notification(ndb.Model):
    username = ndb.StringProperty(indexed=True)
    time = ndb.DateTimeProperty(auto_now=True)
    text = ndb.StringProperty()
    url = ndb.StringProperty()
    is_read = ndb.BooleanProperty(indexed=True)
