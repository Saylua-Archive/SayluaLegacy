from google.appengine.ext import ndb

from saylua import db


class Conversation(db.Model):
    __tablename__ = "conversations"

    id = db.Column(db.Integer, primary_key=True)

    def url(self):
        return '/conversation/' + str(self.id) + '/'


class ConversationHandle(db.Model):
    __tablename__ = "conversation_handles"

    conversation_id = db.Column(db.Integer, db.ForeignKey('conversations.id'), primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)

    title = db.Column(db.String(256))
    unread = db.Column(db.Boolean, default=False)
    hidden = db.Column(db.Boolean, default=False)
    last_updated = db.Column(db.DateTime(timezone=True), server_default=db.func.now())

    def url(self):
        if self.unread:
            return '/conversation_read/' + str(self.conversation_id) + '/'
        return '/conversation/' + str(self.conversation_id) + '/'


class Message(db.Model):
    __tablename__ = "messages"

    id = db.Column(db.Integer, primary_key=True)
    conversation_id = db.Column(db.Integer, db.ForeignKey('conversations.id'))
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    text = db.Column(db.Text())
    date_created = db.Column(db.DateTime(timezone=True), server_default=db.func.now())


class _Notification(db.Model):
    __tablename__ = "notifications"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    time = db.Column(db.DateTime(timezone=True), server_default=db.func.now())
    text = db.Column(db.Text())
    unread = db.Column(db.Boolean, default=True)
    link = db.Column(db.String(512))
    count = db.Column(db.Integer)


class Notification(ndb.Model):
    user_id = ndb.IntegerProperty()
    time = ndb.DateTimeProperty(auto_now_add=True)
    text = ndb.StringProperty()
    link = ndb.StringProperty()
    is_read = ndb.BooleanProperty(default=False)
    count = ndb.IntegerProperty(default=1)

    @classmethod
    def send(cls, user_id, text, link):
        notification = cls.query(cls.user_id == user_id,
            cls.text == text, cls.link == link, cls.is_read == False).get()
        if not notification:
            notification = cls(user_id=user_id, text=text, link=link)
        else:
            notification.count += 1
        return notification.put()
