from saylua import app
from saylua.utils import saylua_time, pluralize
from dateutil import tz
import datetime
from flask import request, render_template

@app.template_filter('pluralize')
def saylua_pluralize(count, singular_noun, plural_noun=None):
    return pluralize(count, singular_noun, plural_noun)

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

@app.template_filter('relative_time')
def saylua_relative_time(d):
    diff = datetime.datetime.now() - d
    s = diff.seconds
    if diff.days > 7 or diff.days < 0:
        return template_show_datetime(d)
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
