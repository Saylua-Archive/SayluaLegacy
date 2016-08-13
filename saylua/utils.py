from google.appengine.ext import ndb

def make_ndb_key(key_string):
    return ndb.Key(urlsafe=key_string)
