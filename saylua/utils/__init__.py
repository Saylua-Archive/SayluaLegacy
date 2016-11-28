from google.appengine.ext import ndb
from dateutil import tz
import re


def make_ndb_key(key_string):
    try:
        key = ndb.Key(urlsafe=key_string)
    except Exception:
        return None
    return key


def pluralize(count, singular_noun, plural_noun=None):
    if not plural_noun:
        plural_noun = singular_noun + 's'
    if count == 1:
        return str(count) + ' ' + singular_noun
    return str(count) + ' ' + plural_noun


def saylua_time(time):
    from_zone = tz.gettz('UTC')
    to_zone = tz.gettz('America/New_York')
    time = time.replace(tzinfo=from_zone)
    return time.astimezone(to_zone)


def get_from_request(request, key, form_key=None, args_key=None):
    if not args_key:
        args_key = key
    if not form_key:
        form_key = key
    result = ''
    if form_key in request.form:
        result = request.form.get(form_key)
    elif request.args.get(args_key):
        result = request.args.get(args_key)
    return result


def urlize(s):
    s = re.sub('[^0-9a-zA-Z]+', '_', s).lower()
    return s
