from google.appengine.ext import ndb
import user

class Message(ndb.Model):
    time = ndb.DateTimeProperty(auto_now=True)
    title = ndb.StringProperty()

class MessagePost(ndb.Model):
    text = ndb.StringProperty()
    time = ndb.DateTimeProperty(indexed=True, auto_now_add=True)

class MessageUser(ndb.Model):
    user = ndb.KeyProperty(indexed=True)
    message = ndb.KeyProperty(indexed=True)
    read = ndb.BooleanProperty()
    deleted = ndb.BooleanProperty(default=False)
    time = ndb.DateTimeProperty(indexed=True, auto_now=True)
