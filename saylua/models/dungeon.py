from google.appengine.ext import ndb

# Consider using PickleProperty with compress=True in the future.
# As even the largest concievable tilemap would take up at most ~1.5MB,
# it would take ~700 users (1GB of data) before the issue of diskspace
# might be worth addressing.
#
# This is assuming a tile size 10 times larger than they currently are,
# with no cycling. (Dungeons should be depopulated based on inactivity)


class Dungeon(ndb.Model):
  user_key = ndb.KeyProperty(indexed=True)
  name = ndb.StringProperty()
  last_accessed = ndb.DateTimeProperty(auto_now_add=True)
  tile_layer = ndb.BlobProperty()
  entity_layer = ndb.BlobProperty()

  # Usefulness of this method is questionable.
  @classmethod
  def create(cls, user_key, name, tile_layer, entity_layer):
    dungeon = cls(user_key=user_key, name=name, tile_layer=tile_layer,
                  entity_layer=entity_layer)
    return dungeon.put()
