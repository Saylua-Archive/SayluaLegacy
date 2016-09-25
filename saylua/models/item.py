from google.appengine.ext import ndb
from protorpc import messages

class ItemType(messages.Enum):
    food = 1
    clothing = 2
    equipment = 3
    hardware = 4
    materials = 5
    special = 6

# StructuredProperty for Conversation
class AvatarItemImage(ndb.Model):
    front_image = ndb.StringProperty()
    back_image = ndb.StringProperty()

class Item(ndb.Model):
    name = ndb.StringProperty(indexed=True)
    image_url = ndb.StringProperty()
    description = ndb.StringProperty()
    category = ndb.EnumProperty(ItemType, repeated=True)

    masculine_image = ndb.StructuredProperty(AvatarItemImage)
    feminine_image = ndb.StructuredProperty(AvatarItemImage)

class InventoryItem(ndb.Model):
    name = ndb.StringProperty(indexed=True)
    image_url = ndb.StringProperty()
    description = ndb.StringProperty()
    category = ndb.EnumProperty(ItemType, repeated=True)

    user_key = ndb.KeyProperty(indexed=True)
    item_key = ndb.KeyProperty(indexed=True)

    # Note that when we update the name/image for an item we need to update it for all users
    count = ndb.IntegerProperty()
