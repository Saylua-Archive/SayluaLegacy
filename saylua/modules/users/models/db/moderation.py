from saylua import db
import datetime


class BanTypes:
    BAN = 0
    MUTE = 1


class BanLog(db.Model):
    """A history of times users have been banned or muted.
    """
    __tablename__ = "ban_logs"

    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(db.Integer, db.ForeignKey("users.id", name="banned_user"))
    user = db.relationship("User", foreign_keys=[user_id])

    # 0 is a default ban.
    ban_type = db.Column(db.Integer)
    is_permanent = db.Column(db.Boolean, default=False)
    banned_until = db.Column(db.DateTime)
    reason = db.Column(db.Text)

    date_banned = db.Column(db.DateTime, server_default=db.func.now())
    date_modified = db.Column(db.DateTime, onupdate=db.func.now())

    # Only set if a user is manually unbanned.
    date_unbanned = db.Column(db.DateTime)

    def active(self):
        return self.is_permanent or (self.banned_until and self.banned_until > datetime.datetime.now())

    def verb(self):
        if self.ban_type == BanTypes.MUTE:
            return 'mute'
        return 'ban'

    def past_tense(self):
        if self.ban_type == BanTypes.MUTE:
            return 'muted'
        return 'banned'
