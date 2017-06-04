from saylua import db


class RUserTitles(db.Model):
    __tablename__ = 'r_user_titles'

    user_id = db.Column('user_id', db.Integer, db.ForeignKey('users.id'), primary_key=True)
    title_id = db.Column('title_id', db.Integer, db.ForeignKey('titles.id'), primary_key=True)


class Title(db.Model):
    """Defines titles that users can hold.
    Examples of titles: admin, programmer, artist, contributor

    Many to one with Users.
    """

    __tablename__ = "titles"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(256), unique=True)
    canon_name = db.Column(db.String(256), unique=True)

    users = db.relationship("User",
        secondary='r_user_titles',
        back_populates="titles",
        lazy='dynamic'
    )

    def css_class(self):
        return 'title-' + self.canon_name
