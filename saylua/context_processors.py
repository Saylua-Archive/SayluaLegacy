from saylua import app
from saylua.modules.users.models.db import User
from saylua.modules.messages.models.db import ConversationHandle
from saylua.modules.messages.models.db import Notification
from saylua.utils import get_static_version_id, truncate

from flask import g, url_for
from saylua import db

from functools import partial

import os
import random
import datetime


# Injected functions.

@app.context_processor
def inject_include_static():
    def include_static(file_path):
        return url_for('static', filename=file_path) + '?v=' + str(get_static_version_id())

    return dict(include_static=include_static)


@app.context_processor
def inject_random_image():
    def random_image(folder_name):
        subpath = 'img' + os.sep + folder_name + os.sep
        path = os.path.join(app.static_folder, subpath)
        return random_image_helper(path)

    return dict(random_pet_image=partial(random_image, 'pets'),
        random_item_image=partial(random_image, 'items'),
        random_character_image=partial(random_image, 'characters'),
        random_mini_image=partial(random_image, 'items/minis'),
        random_background_image=partial(random_image, 'backgrounds'),
        random_icon_image=partial(random_image, 'icons'))


def random_image_helper(folder):
    name = random.choice(os.listdir(folder))
    name_path = folder + name
    subpath = name_path[name_path.rfind("static" + os.sep) + 7:]
    if os.path.isdir(name_path):
        return random_image_helper(name_path + os.sep)
    elif name.endswith(".png") or name.endswith(".jpg"):
        return (url_for('static', filename=subpath) +
            '?v=' + str(get_static_version_id()))
    else:
        return random_image_helper(folder)


@app.context_processor
def inject_truncate():
    return dict(truncate=truncate)


# Injected variables.

@app.context_processor
def inject_version_id():
    return dict(version_id=get_static_version_id())


@app.context_processor
def inject_notifications():
    if not g.logged_in:
        return {}
    notifications_count = (
        db.session.query(Notification.id)
        .filter(Notification.user_id == g.user.id)
        .filter(Notification.unread == True)
        .limit(100)
        .count()
    )
    notifications = (
        db.session.query(Notification)
        .filter(Notification.user_id == g.user.id)
        .filter(Notification.unread)
        .order_by(Notification.time.desc())
        .limit(5)
        .all()
    )
    if not notifications:
        notifications = []
    return dict(notifications_count=notifications_count, notifications=notifications)


@app.context_processor
def inject_messages():
    if not g.logged_in:
        return {}
    nav_messages_count = (
        db.session.query(ConversationHandle.conversation_id)
        .filter(ConversationHandle.user_id == g.user.id)
        .filter(ConversationHandle.hidden == False)
        .filter(ConversationHandle.unread == True)
        .count()
    )
    nav_messages = (
        db.session.query(ConversationHandle)
        .filter(ConversationHandle.user_id == g.user.id)
        .filter(ConversationHandle.hidden == False)
        .order_by(ConversationHandle.last_updated.desc())
        .order_by(ConversationHandle.unread)
        .limit(5)
        .all()
    )
    if not nav_messages:
        nav_messages = []
    return dict(nav_messages_count=nav_messages_count, nav_messages=nav_messages)


@app.context_processor
def inject_time():
    return dict(saylua_time=datetime.datetime.now())


@app.context_processor
def inject_users_online():
    mins_ago = datetime.datetime.now() - datetime.timedelta(
        minutes=app.config['USERS_ONLINE_RANGE'])

    user_count = (
        db.session.query(User.id)
        .filter(User.last_action >= mins_ago)
        .count()
    )

    return dict(users_online_count=user_count)
