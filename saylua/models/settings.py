from google.appengine.ext import ndb


# This is a model for the global settings used across the site
class Settings(ndb.Model):
    name = ndb.StringProperty()
    value = ndb.StringProperty()
