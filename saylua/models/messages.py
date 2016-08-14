from google.appengine.ext import ndb
from saylua.models.user import User

class Conversation(ndb.Model):
    title = ndb.StringProperty()

class ConversationMessage(ndb.Model):
    user = ndb.KeyProperty(indexed=True)
    text = ndb.StringProperty()
    time = ndb.DateTimeProperty(indexed=True, auto_now_add=True)

class ConversationUser(ndb.Model):
    user = ndb.KeyProperty(indexed=True)
    conversation = ndb.KeyProperty(indexed=True)
    conversation_title = ndb.StringProperty()
    is_read = ndb.BooleanProperty(default=False)
    is_deleted = ndb.BooleanProperty(default=False)
    time = ndb.DateTimeProperty(indexed=True, auto_now=True)
