from saylua import app, db
from saylua.utils import canonize, is_devserver, get_static_version_id, go_up
from flask import url_for
import os


class ItemCategory:
    categories = ["food", "gifts", "materials", "minis", "clothes"]

    def __init__(self, category):
        if isinstance(category, basestring):
            self.id = ItemCategory.categories.index(category)
        else:
            self.id = category

    def __eq__(self, other):
        return other == self.id or other == self.name()

    def name(self):
        if self.id >= 0 and self.id < len(ItemCategory.categories):
            return ItemCategory.categories[self.id]
        return ''

    @classmethod
    def get_categories(cls):
        return cls.categories


class Item(db.Model):
    __tablename__ = "items"

    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(256), unique=True)
    canon_name = db.Column(db.String(256), unique=True)
    description = db.Column(db.String(1024))

    category_id = db.Column(db.Integer)

    def url(self):
        return '/item/' + self.canon_name

    def image_url(self):
        if is_devserver():
            category_name = self.category_name()
            subpath = ("img" + os.sep + "items" + os.sep + category_name +
                os.sep + self.canon_name + ".png")
            image_path = (os.path.join(go_up(4, (__file__)), "static", subpath))
            if os.path.isfile(image_path):
                return url_for("static", filename=subpath) + "?v=" + str(get_static_version_id())
        return (app.config['IMAGE_BUCKET_ROOT'] + "/items/" + self.canon_name +
            ".png?v=" + str(get_static_version_id()))

    def category_name(self):
        return ItemCategory(self.category_id).name()

    def grant(self, user_id, count):
        inventory_entry = InventoryItem.by_user_item(user_id, self.id)
        if not inventory_entry:
            inventory_entry = InventoryItem(user_id=user_id, item_id=self.id)
        inventory_entry.count += count
        inventory_entry.put()

    @classmethod
    def make_canon_name(cls, name):
        return canonize(name)

    @classmethod
    def by_canon_name(cls, name):
        return db.session.query(cls).filter(cls.canon_name == name.lower()).one_or_none()


class InventoryItem(db.Model):
    __tablename__ = "inventory_items"

    # These two keys define the inventory item entry.
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)
    user = db.relationship("User")

    item_id = db.Column(db.Integer, db.ForeignKey('items.id'), primary_key=True)
    item = db.relationship("Item")

    count = db.Column(db.Integer, default=0)
