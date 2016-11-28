from google.appengine.ext import ndb

import re


# StructuredProperty for Conversation
class ItemAvatarData(ndb.Model):
    f_front_image = ndb.StringProperty()
    f_back_image = ndb.StringProperty()
    m_front_image = ndb.StringProperty()
    m_back_image = ndb.StringProperty()


class Item(ndb.Model):
    name = ndb.StringProperty()
    url_name = ndb.StringProperty()
    image_url = ndb.StringProperty()
    description = ndb.StringProperty()

    # Denormalized data for specific item use cases
    avatar_data = ndb.KeyProperty()

    @classmethod
    def create(cls, name, image_url, description):
        return cls(name=name, image_url=image_url, description=description,
            url_name=cls.make_url_name(name))

    @classmethod
    def make_url_name(cls, name):
        name = re.sub(r'\s', '_', name)
        name = re.sub(r'\W', '-', name)
        return name.lower()

    @classmethod
    def by_url_name(cls, name):
        return cls.query(cls.url_name==name.lower()).get()

    @classmethod
    def update_item(cls, item, name, image_url, description):
        item.name = name
        item.image_url = image_url
        item.description = description

        # TODO: Update the denormalized versions of this data in everyone's inventory

    @classmethod
    def give_item(cls, user_key, item, count):
        inventory_entry = InventoryItem.by_user_item(user_key, item.key)
        if not inventory_entry:
            inventory_entry = InventoryItem.construct(user_key, item)
        inventory_entry.count += count
        inventory_entry.put()


class InventoryItem(ndb.Model):
    # This data is all denormalized. Must update when the main item data is
    # updated.
    name = ndb.StringProperty()
    image_url = ndb.StringProperty()
    description = ndb.StringProperty()

    avatar_data = ndb.KeyProperty()

    # These two keys define the inventory item entry.
    user_key = ndb.KeyProperty()
    item_key = ndb.KeyProperty()

    count = ndb.IntegerProperty()

    @classmethod
    def construct(cls, user_key, item):
        return cls(name=item.name, image_url=item.image_url, description=item.description,
            category=item.category, user_key=user_key, item_key=item.key)

    @classmethod
    def by_user_item(cls, user_key, item_key):
        return cls.query(cls.user_key==user_key, cls.item_key==item_key).get()
