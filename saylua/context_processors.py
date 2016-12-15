from saylua import app
from saylua.models.user import User
from saylua.modules.messages.models.db import UserConversation
from saylua.modules.messages.models.db import Notification
from saylua.utils import get_static_version_id, include_static

from flask import g

import datetime


@app.context_processor
def inject_version_id():
    return dict(version_id=get_static_version_id())


@app.context_processor
def inject_include_static():
    return dict(include_static=include_static)


@app.context_processor
def inject_notifications():
    if not g.logged_in:
        return {}
    notifications_count = Notification.query(Notification.user_key == g.user.key,
        Notification.is_read == False).count(limit=100)
    notifications = Notification.query(Notification.user_key == g.user.key).order(
        Notification.is_read, -Notification.time).fetch(limit=5)
    if not notifications:
        notifications = []
    return dict(notifications_count=notifications_count, notifications=notifications)


@app.context_processor
def inject_messages():
    if not g.logged_in:
        return {}
    messages_count = UserConversation.query(
        UserConversation.user_key == g.user.key,
        UserConversation.is_read == False,
        UserConversation.is_deleted == False).count(limit=100)
    messages = UserConversation.query(UserConversation.user_key == g.user.key,
        UserConversation.is_deleted == False).order(
        UserConversation.is_read, -UserConversation.time).fetch(limit=5)
    if not messages:
        messages = []
    return dict(messages_count=messages_count, messages=messages)


@app.context_processor
def inject_time():
    return dict(saylua_time=datetime.datetime.now())


@app.context_processor
def inject_users_online():
    mins_ago = datetime.datetime.now() - datetime.timedelta(
        minutes=app.config['USERS_ONLINE_RANGE'])
    user_count = User.query(User.last_action >= mins_ago).count()
    return dict(users_online_count=user_count)
