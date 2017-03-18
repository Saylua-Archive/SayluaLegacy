from saylua import app, db
from saylua.models.user import User
from saylua.utils import pluralize, saylua_time
from saylua.modules.forums.models.db import ForumPost, ForumThread

from flask_markdown import Markdown

import datetime


# Attach Flask Markdown to our app.
Markdown(app, auto_reset=True, extensions=["linkify"])


@app.template_filter('pluralize')
def saylua_pluralize(count, singular_noun, plural_noun=None):
    return pluralize(count, singular_noun, plural_noun)


# Convert key to urlsafe string
@app.template_filter('make_urlsafe')
def saylua_make_urlsafe(key):
    return key.urlsafe()


# Time filters
@app.template_filter('show_date')
def saylua_show_date(time):
    time = saylua_time(time)
    return time.strftime('%b %d, %Y')


@app.template_filter('show_time')
def saylua_show_time(time):
    time = saylua_time(time)
    return time.strftime('%I:%M:%S %p SMT')


@app.template_filter('show_datetime')
def saylua_show_datetime(time):
    time = saylua_time(time)
    return time.strftime('%b %d, %Y %I:%M %p SMT')


@app.template_filter('expanded_relative_time')
def saylua_expanded_relative_time(d):
    diff = datetime.datetime.now() - d
    result = saylua_show_datetime(d)
    if diff.days >= 0 and diff.days <= 7:
        result += ' (' + saylua_relative_time(d) + ')'
    return result


@app.template_filter('relative_time')
def saylua_relative_time(d):
    diff = datetime.datetime.now() - d
    s = diff.seconds
    if diff.days > 7 or diff.days < 0:
        return saylua_show_datetime(d)
    elif diff.days == 1:
        return '1 day ago'
    elif diff.days > 1:
        return '{} days ago'.format(diff.days)
    elif s <= 1:
        return 'just now'
    elif s < 60:
        return '{} seconds ago'.format(s)
    elif s < 120:
        return '1 minute ago'
    elif s < 3600:
        return '{} minutes ago'.format(s / 60)
    elif s < 7200:
        return '1 hour ago'
    else:
        return '{} hours ago'.format(s / 3600)


# Filters that act on models
@app.template_filter('message_status')
def saylua_message_status(user_conversation):
    if user_conversation.is_deleted:
        return 'deleted'
    if not user_conversation.is_read:
        return 'unread'
    if user_conversation.is_first:
        return 'sent'
    if user_conversation.is_replied:
        return 'replied'
    return 'read'


@app.template_filter('user_url')
def saylua_user_url(user):
    return '/user/' + user.name().lower() + '/'


# Conversation can be either a ConversationUser or Conversation model.
@app.template_filter('conversation_url')
def saylua_conversation_url(conversation):
    c_id = conversation.id
    if hasattr(conversation, 'conversation_id'):
        # This is the case if this is acting on a ConversationUser object instead
        # of a Conversation object.
        c_id = conversation.conversation_id
    elif not conversation.is_read:
        # This case can only happen on a UserConversation object
        return '/conversation_read/' + str(c_id) + '/'

    return '/conversation/' + str(c_id) + '/'


# Query filters. Use these only when necessary.
@app.template_filter('user_from_id')
def user_from_id(user_id):
    user = (
        db.session.query(User)
        .filter(User.id == user_id)
        .one_or_none()
    )

    return user


@app.template_filter('name_from_author_id')
def display_name_from_user_id(user_id):
    user = user_from_id(user_id)
    if user:
        return user.name()

    return "Unknown User"


@app.template_filter('last_post_thread')
def last_post_thread(thread_id):
    return (
        db.session.query(ForumPost)
        .filter(ForumPost.thread_id == thread_id)
        .order_by(ForumPost.date_modified.desc())
        .first()
    )


@app.template_filter('last_post_board')
def last_post_board(board_id):
    return (
        db.session.query(ForumPost)
        .join(ForumThread, ForumPost.thread)
        .filter(ForumThread.board_id == board_id)
        .order_by(ForumPost.date_modified.desc())
        .first()
    )


@app.template_filter('thread_by_id')
def thread_by_id(thread_id):
    return (
        db.session.query(ForumThread)
        .filter(ForumThread.id == thread_id)
        .first()
    )


@app.template_filter('count_thread_posts')
def count_thread_posts(thread_id):
    return (
        db.session.query(ForumPost)
        .filter(ForumPost.thread_id == thread_id)
        .count()
    )


@app.template_filter('count_board_posts')
def count_board_posts(board_id):
    return (
        db.session.query(ForumPost)
        .join(ForumThread, ForumPost.thread)
        .filter(ForumThread.board_id == board_id)
        .count()
    )


@app.template_filter('count_board_threads')
def count_board_threads(board_id):
    return (
        db.session.query(ForumThread)
        .filter(ForumThread.board_id == board_id)
        .count()
    )
