from google.appengine.ext import ndb

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
