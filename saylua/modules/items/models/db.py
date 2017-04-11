import re

from saylua import db


class Item(db.Model):
    __tablename__ = "items"

    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(256), unique=True)
    url_name = db.Column(db.String(256), unique=True)
    image_url = db.Column(db.String(256))
    description = db.Column(db.String(1024))

    @classmethod
    def make_url_name(cls, name):
        name = re.sub(r'\s', '_', name)
        name = re.sub(r'\W', '-', name)
        return name.lower()

    @classmethod
    def by_url_name(cls, name):
        return cls.query(cls.url_name == name.lower()).get()

    @classmethod
    def update_item(cls, item, name, image_url, description):
        item.name = name
        item.image_url = image_url
        item.description = description

        # TODO: Update the denormalized versions of this data in everyone's inventory

    @classmethod
    def give_item(cls, user_id, item, count):
        inventory_entry = InventoryItem.by_user_item(user_id, item.key)
        if not inventory_entry:
            inventory_entry = InventoryItem.construct(user_id, item)
        inventory_entry.count += count
        inventory_entry.put()


class InventoryItem(db.Model):
    __tablename__ = "inventory_items"

    # These two keys define the inventory item entry.
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)
    item_id = db.Column(db.Integer, db.ForeignKey('items.id'), primary_key=True)

    count = db.Column(db.Integer)

    @classmethod
    def by_user_item(cls, user_id, item_key):
        return cls.query(cls.user_id == user_id, cls.item_key == item_key).get()
