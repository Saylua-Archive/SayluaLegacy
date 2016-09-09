from saylua import app
from saylua.utils import saylua_time, pluralize
from saylua.models.user import User
from dateutil import tz
import datetime
from flask import request, render_template

@app.template_filter('pluralize')
def saylua_pluralize(count, singular_noun, plural_noun=None):
    return pluralize(count, singular_noun, plural_noun)

# Time filters

@app.template_filter('show_date')
def saylua_show_date(time):
    time = saylua_time(time)
    return time.strftime('%b %d, %Y')

@app.template_filter('show_time')
def saylua_show_time(time):
    time = saylua_time(time)
    return time.strftime('%I:%M:%S %p SST')

@app.template_filter('show_datetime')
def saylua_show_datetime(time):
    time = saylua_time(time)
    return time.strftime('%b %d, %Y %I:%M %p SST')

@app.template_filter('expanded_relative_time')
def saylua_expanded_relative_time(d):
    diff = datetime.datetime.now() - d
    s = diff.seconds
    result = saylua_show_datetime(d)
    if diff.days >= 0 or diff.days <= 7:
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
def saylua_message_status(conversation_user):
    if conversation_user.is_deleted:
        return 'deleted'
    if not conversation_user.is_read:
        return 'unread'
    if conversation_user.is_first:
        return 'sent'
    if conversation_user.is_replied:
        return 'replied'
    return 'read'

@app.template_filter('user_url')
def saylua_user_url(user):
    return '/user/' + user.username + '/'

# conversation can be either a ConversationUser or Conversation model
@app.template_filter('conversation_url')
def saylua_conversation_url(conversation):
    key = conversation.conversation_key
    if not key:
        # This is the case if this is acting on a Conversation object instead of
        # a ConversationUser object
        key = conversation.key
    elif not conversation.is_read:
        # This case can only happen on a ConversationUser object
        return '/conversation_read/' + key.urlsafe() + '/'

    return '/conversation/' + key.urlsafe() + '/'


# Query filters. Use these only when necessary.
@app.template_filter('user_object')
def saylua_user_object(user_key):
    return User.get_by_id(user_key.id())
