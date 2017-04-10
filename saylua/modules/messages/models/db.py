from google.appengine.ext import ndb
from flask import flash
from saylua import db

import flask_sqlalchemy


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

    @classmethod
    def read_conversations(cls, keys, user_id):
        if isinstance(keys, (int, long)): # noqa
            keys = [keys]
        for key in keys:
            try:
                found_conversation = db.session.query(cls).get((key, user_id))
                found_conversation.unread = False
                db.session.add(found_conversation)
            except(flask_sqlalchemy.orm.exc.NoResultFound):
                flash('Message read failed for an unexpected reason.', 'error')
                return False
        db.session.commit()
        return True

    # This marks a user conversation as hidden, it will be unhidden if a new reply is made.
    @classmethod
    def hide_conversations(cls, keys, user_id):
        if isinstance(keys, (int, long)): # noqa
            keys = [keys]
        for key in keys:
            try:
                found_conversation = db.session.query(cls).get((key, user_id))
                found_conversation.hidden = True
                db.session.add(found_conversation)
            except(flask_sqlalchemy.orm.exc.NoResultFound):
                flash('Message hide failed for an unexpected reason.', 'error')
                return False
        db.session.commit()
        return True


class Message(db.Model):
    __tablename__ = "messages"

    id = db.Column(db.Integer, primary_key=True)
    conversation_id = db.Column(db.Integer, db.ForeignKey('conversations.id'))
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    text = db.Column(db.Text())
    date_created = db.Column(db.DateTime(timezone=True), server_default=db.func.now())


class Notification(db.Model):
    __tablename__ = "notifications"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    time = db.Column(db.DateTime(timezone=True), server_default=db.func.now())
    text = db.Column(db.Text())
    unread = db.Column(db.Boolean, default=True)
    link = db.Column(db.String(512))
    count = db.Column(db.Integer)

    @classmethod
    def send(cls, user_id, text, link):
        notification = cls.query(cls.user_id == user_id,
            cls.text == text, cls.link == link, cls.is_read == False).get()
        if not notification:
            notification = cls(user_id=user_id, text=text, link=link)
        else:
            notification.count += 1
        return notification.put()


class _Notification(ndb.Model):
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
