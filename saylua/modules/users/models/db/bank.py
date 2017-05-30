from saylua import db


class BankAccount(db.Model):
    """Permanently assigned bank account for the `User` class.

    One to one relationship with `User`.
    """

    __tablename__ = "bank_accounts"

    id = db.Column(db.Integer, db.ForeignKey("users.id"), primary_key=True)
    user = db.relationship("User", back_populates="bank_account")

    star_shards = db.Column(db.Integer, default=0)
    cloud_coins = db.Column(db.Integer, default=0)
