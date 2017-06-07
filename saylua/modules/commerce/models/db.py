from saylua import db


class BankTransfer(db.Model):

    __tablename__ = "bank_transfers"

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)

    sender_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    recipient_id = db.Column(db.Integer, db.ForeignKey("users.id"))

    star_shards = db.Column(db.Integer, default=0)
    cloud_coins = db.Column(db.Integer, default=0)

    date_transferred = db.Column(db.DateTime, server_default=db.func.now())
