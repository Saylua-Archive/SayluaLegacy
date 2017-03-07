from saylua import app
from saylua.models.user import User
from saylua.modules.messages.models.db import UserConversation
from saylua.modules.messages.models.db import Notification
from saylua.utils import get_static_version_id

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
    def random_image(folder):
        subpath = 'img/' + folder + '/'
        path = os.path.join(app.static_folder, subpath)
        name = None
        while not name or name == '.DS_Store':
            name = random.choice(os.listdir(path))
        return (url_for('static', filename=subpath + name) +
            '?v=' + str(get_static_version_id()))

    return dict(random_pet_image=partial(random_image, 'pets'),
        random_item_image=partial(random_image, 'items'),
        random_character_image=partial(random_image, 'characters'),
        random_mini_image=partial(random_image, 'minis'),
        random_background_image=partial(random_image, 'backgrounds'),
        random_icon_image=partial(random_image, 'icons'))


@app.context_processor
def inject_truncate():
    def truncate(s, maxlen=50):
        if len(s) > maxlen:
            return (s[:maxlen] + '...')
        return s
    return dict(truncate=truncate)


@app.context_processor
def inject_get_user_from_id():
    def user_from_id(id):
        return (
            db.session.query(User)
            .filter(User.id == id)
            .one_or_none()
        )
    return dict(user_from_id=user_from_id)


# Injected variables.

@app.context_processor
def inject_version_id():
    return dict(version_id=get_static_version_id())


@app.context_processor
def inject_notifications():
    if not g.logged_in:
        return {}
    notifications_count = Notification.query(Notification.user_id == g.user.id,
        Notification.is_read == False).count(limit=100)
    notifications = Notification.query(Notification.user_id == g.user.id).order(
        Notification.is_read, -Notification.time).fetch(limit=5)
    if not notifications:
        notifications = []
    return dict(notifications_count=notifications_count, notifications=notifications)


@app.context_processor
def inject_messages():
    if not g.logged_in:
        return {}
    messages_count = UserConversation.query(
        UserConversation.user_id == g.user.id,
        UserConversation.is_read == False,
        UserConversation.is_deleted == False).count(limit=100)
    messages = UserConversation.query(UserConversation.user_id == g.user.id,
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

    user_count = (
        db.session.query(User)
        .filter(User.last_action >= mins_ago)
        .count()
    )

    return dict(users_online_count=user_count)
