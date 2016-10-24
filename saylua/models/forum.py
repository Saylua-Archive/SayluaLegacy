from google.appengine.ext import ndb

class Board(ndb.Model):
    title = ndb.StringProperty(indexed=True)
    url_title = ndb.StringProperty()
    board_id = ndb.StringProperty()
    category_key = ndb.StringProperty(indexed=True)
    description = ndb.TextProperty()

class BoardCategory(ndb.Model):
    title = ndb.StringProperty(indexed=True)

class ForumThread(ndb.Model):
    creator_key = ndb.StringProperty(indexed=True)
    created_time = ndb.DateTimeProperty(auto_now_add=True)
    last_action = ndb.DateTimeProperty(auto_now=True)
    board_id = ndb.IntegerProperty()
    title = ndb.StringProperty()
    is_pinned = ndb.BooleanProperty(default=False)
    is_locked = ndb.BooleanProperty(default=False)

class ForumPost(ndb.Model):
    creator_key = ndb.StringProperty(indexed=True)
    thread_id = ndb.IntegerProperty()
    board_id = ndb.IntegerProperty()
    body = ndb.TextProperty()
    created_time = ndb.DateTimeProperty(auto_now_add=True)
