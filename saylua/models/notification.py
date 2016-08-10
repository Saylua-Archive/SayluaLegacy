from google.appengine.ext import ndb
import user

class Notification(ndb.Model):
    user = ndb.KeyProperty(indexed=True)
    time = ndb.DateTimeProperty(auto_now_add=True)
    text = ndb.StringProperty()
    url = ndb.StringProperty()
    is_read = ndb.BooleanProperty(indexed=True)
