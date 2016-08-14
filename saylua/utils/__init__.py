from google.appengine.ext import ndb
from dateutil import tz

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
    time = time.replace(tzinfo = from_zone)
    return time.astimezone(to_zone)
