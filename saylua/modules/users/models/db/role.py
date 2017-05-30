from saylua import db


r_user_titles = db.Table('r_user_titles',
    db.Column('user_id', db.Integer, db.ForeignKey('users.id')),
    db.Column('title_id', db.Integer, db.ForeignKey('titles.id'))
)


class Title(db.Model):
    """Defines permissions for users.

    Many to many with Users.
    """

    __tablename__ = "titles"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(256), unique=True)
    color = db.Column(db.String(256))

    users = db.relationship("User",
        secondary=r_user_titles,
        back_populates="titles",
        lazy='dynamic'
    )


class Role(db.Model):
    """Defines permissions for users.

    No explicit relationships exist between this and any
    other model.
    """

    __tablename__ = "roles"

    name = db.Column(db.String(256), primary_key=True)

    # Access to forum moderation features.
    can_moderate = db.Column(db.Boolean, default=False)

    # This give access to anything you can do on the site.
    # Note: For now granting roles is done through only the database.
    can_admin = db.Column(db.Boolean, default=False)
