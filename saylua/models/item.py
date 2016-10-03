from google.appengine.ext import ndb

class Item(ndb.Model):
    name = ndb.StringProperty(indexed=True)
    image_url = ndb.StringProperty()

class InventoryItem(ndb.Model):
    user_key = ndb.KeyProperty(indexed=True)
    item_key = ndb.KeyProperty(indexed=True)

    # Note that when we update the name/image for an item we need to update it for all users
    name = ndb.StringProperty(indexed=True)
    image_url = ndb.StringProperty()
    count = ndb.IntegerProperty()
