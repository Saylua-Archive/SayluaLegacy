import re

from saylua import db


class Item(db.Model):
    __tablename__ = "items"

    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(256), unique=True)
    text_id = db.Column(db.String(256), unique=True)
    description = db.Column(db.String(1024))

    @classmethod
    def make_text_id(cls, name):
        name = re.sub(r'\s', '_', name)
        name = re.sub(r'\W', '-', name)
        return name.lower()

    @classmethod
    def by_text_id(cls, name):
        return cls.query(cls.text_id == name.lower()).get()

    def url(self):
        return '/item/' + self.text_id

    def image_url(self):
        return '/static/img/items/' + self.text_id + '.png'

    def grant(self, user_id, count):
        inventory_entry = InventoryItem.by_user_item(user_id, self.id)
        if not inventory_entry:
            inventory_entry = InventoryItem(user_id=user_id, item_id=self.id)
        inventory_entry.count += count
        inventory_entry.put()


class InventoryItem(db.Model):
    __tablename__ = "inventory_items"

    # These two keys define the inventory item entry.
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)
    user = db.relationship("User")

    item_id = db.Column(db.Integer, db.ForeignKey('items.id'), primary_key=True)
    item = db.relationship("Item")

    count = db.Column(db.Integer, default=0)
