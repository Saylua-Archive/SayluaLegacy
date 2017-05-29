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

    user = db.relationship("User")

    title = db.Column(db.String(256))
    unread = db.Column(db.Boolean, default=False)
    hidden = db.Column(db.Boolean, default=False)
    last_updated = db.Column(db.DateTime, server_default=db.func.now())

    def url(self):
        if self.unread:
            return '/conversation_read/' + str(self.conversation_id) + '/'
        return '/conversation/' + str(self.conversation_id) + '/'

    def status(self):
        if self.hidden:
            return 'deleted'
        if self.unread:
            return 'unread'
        return 'read'

    def recipients(self):
        return db.session.query(ConversationHandle).filter(
            ConversationHandle.conversation_id == self.conversation_id).all()

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
    author = db.relationship("User")

    text = db.Column(db.Text())
    date_created = db.Column(db.DateTime, server_default=db.func.now())


class Notification(db.Model):
    __tablename__ = "notifications"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    user = db.relationship("User")

    time = db.Column(db.DateTime, server_default=db.func.now())
    text = db.Column(db.Text())
    unread = db.Column(db.Boolean, default=True)
    link = db.Column(db.String(512))
    count = db.Column(db.Integer, default=1)

    @classmethod
    def send(cls, user_id, text, link):
        notification = (
            db.session.query(cls)
            .filter(cls.user_id == user_id)
            .filter(cls.text == text)
            .filter(cls.link == link)
            .filter(cls.unread == True)
            .one_or_none()
        )

        if not notification:
            notification = cls(user_id=user_id, text=text, link=link)
        else:
            notification.count += 1
        db.session.add(notification)
        db.session.commit()
