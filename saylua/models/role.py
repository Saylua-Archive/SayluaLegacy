from saylua import db


class Role(db.Model):
    """Defines permissions for users.

    No explicit relationships exist between this and any
    other model.
    """

    __tablename__ = "roles"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(256), unique=True)

    can_post_threads = db.Column(db.Boolean, default=False)
    can_comment = db.Column(db.Boolean, default=False)
    can_move_threads = db.Column(db.Boolean, default=False)
    can_grant_admin = db.Column(db.Boolean, default=False)
    can_create_roles = db.Column(db.Boolean, default=False)
    can_edit_roles = db.Column(db.Boolean, default=False)
    can_grant_roles = db.Column(db.Boolean, default=False)
    can_access_admin = db.Column(db.Boolean, default=False)
