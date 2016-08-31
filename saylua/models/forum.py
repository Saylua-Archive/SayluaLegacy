from google.appengine.ext import ndb

class Board(ndb.Model):
    title = ndb.StringProperty(indexed=True)
    CategoryKey = ndb.StringProperty(indexed=True)

class BoardCategory(ndb.Model):
    title = ndb.StringProperty(indexed=True)

class ForumThread(ndb.Model):
    creator_key = ndb.StringProperty(indexed=True)
    created_time = ndb.DateTimeProperty(auto_now_add=True)
    title = ndb.StringProperty()
    content = ndb.StringProperty()

class ForumPost(ndb.Model):
    creator_key = ndb.StringProperty(indexed=True)
    created_time = ndb.DateTimeProperty(auto_now_add=True)
    content = ndb.StringProperty()
