from saylua import app
from saylua.utils import make_ndb_key, pluralize, saylua_time
from saylua.modules.forums.models.db import ForumPost, ForumThread

from google.appengine.ext import ndb
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
    return '/user/' + user.display_name.lower() + '/'


# Conversation can be either a UserConversation or Conversation model.
@app.template_filter('conversation_url')
def saylua_conversation_url(conversation):
    key = conversation.conversation_key
    if not key:
        # This is the case if this is acting on a Conversation object instead
        # of a UserConversation object.
        key = conversation.key
    elif not conversation.is_read:
        # This case can only happen on a UserConversation object
        return '/conversation_read/' + key.urlsafe() + '/'

    return '/conversation/' + key.urlsafe() + '/'


# Query filters. Use these only when necessary.
@app.template_filter('name_from_key_string')
def display_name_from_key(user_key):
    u_key = make_ndb_key(user_key)
    found = u_key.get()
    if found:
        return found.display_name
    else:
        return "Unknown User"


@app.template_filter('last_post_thread')
def last_post_thread(thread_id):
    post_query = ForumPost.query(ForumPost.thread_id == thread_id).order(
        -ForumPost.created_time)
    post = post_query.fetch(1)
    if len(post) > 0:
        return post[0]
    return None


@app.template_filter('last_post_board')
def last_post_board(board_id):
    post_query = ForumPost.query(ForumPost.board_id == board_id).order(
        -ForumPost.created_time)
    post = post_query.fetch(1)
    if len(post) > 0:
        return post[0]
    return None


@app.template_filter('thread_by_id')
def thread_by_id(thread_id):
    thread_key = ndb.Key(ForumThread, thread_id)
    return thread_key.get()


@app.template_filter('count_thread_posts')
def count_thread_posts(thread_id):
    return len(ForumPost.query(ForumPost.thread_id == thread_id).fetch(
        keys_only=True))


@app.template_filter('count_board_posts')
def count_board_posts(board_id):
    return len(ForumPost.query(ForumPost.board_id == board_id).fetch(
        keys_only=True))


@app.template_filter('count_board_threads')
def count_board_threads(board_id):
    return len(ForumThread.query(ForumThread.board_id == board_id).fetch(
        keys_only=True))
