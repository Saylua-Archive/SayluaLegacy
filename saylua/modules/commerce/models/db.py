from saylua import db


class BankTransfer(db.Model):

    __tablename__ = "bank_transfers"

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)

    sender_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    recipient_id = db.Column(db.Integer, db.ForeignKey("users.id"))

    star_shards = db.Column(db.Integer, default=0)
    cloud_coins = db.Column(db.Integer, default=0)

    date_transferred = db.Column(db.DateTime, server_default=db.func.now())


class ShopItem(db.Model):
    """
    A model representing a relationship between a shop and its stock.
    """

    __tablename__ = "shop_items"

    shop_id = db.Column(db.Integer, primary_key=True)
    item_id = db.Column(db.Integer, db.ForeignKey("items.id"), primary_key=True)
    item = db.relationship("Item")
