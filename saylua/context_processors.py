from saylua import app
from dateutil import tz
import datetime
from flask import request, g
from saylua.models.messages import ConversationUser
from saylua.models.notification import Notification
from saylua.models.user import User

@app.context_processor
def inject_notifications():
    if not g.logged_in:
        return {}
    notifications_count = Notification.query(Notification.user_key==g.user.key,
        Notification.is_read==False).count(limit=100)
    notifications = Notification.query(Notification.user_key==g.user.key).order(Notification.is_read,
        -Notification.time).fetch(limit=5)
    if not notifications:
        notifications = []
    return dict(notifications_count=notifications_count, notifications=notifications)

@app.context_processor
def inject_messages():
    if not g.logged_in:
        return {}
    messages_count = ConversationUser.query(ConversationUser.user_key==g.user.key,
        ConversationUser.is_read==False).count(limit=100)
    messages = ConversationUser.query(ConversationUser.user_key==g.user.key).order(
        ConversationUser.is_read, -ConversationUser.time).fetch(limit=5)
    if not messages:
        messages = []
    return dict(messages_count=messages_count, messages=messages)

@app.context_processor
def inject_time():
    return dict(saylua_time=datetime.datetime.now())

@app.context_processor
def inject_users_online():
    mins_ago = datetime.datetime.now() - datetime.timedelta(minutes=app.config['USERS_ONLINE_RANGE'])
    user_count = User.query(User.last_action >= mins_ago).count()
    return dict(users_online_count=user_count)
