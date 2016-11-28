from google.appengine.ext import ndb


class Role(ndb.Model):
    can_post_threads = ndb.BooleanProperty(default=False, indexed=False)
    can_comment = ndb.BooleanProperty(default=False, indexed=False)
    can_move_threads = ndb.BooleanProperty(default=False, indexed=False)
    can_grant_admin = ndb.BooleanProperty(default=False, indexed=False)
    can_create_roles = ndb.BooleanProperty(default=False, indexed=False)
    can_edit_roles = ndb.BooleanProperty(default=False, indexed=False)
    can_grant_roles = ndb.BooleanProperty(default=False, indexed=False)
    can_access_admin = ndb.BooleanProperty(default=False, indexed=False)
