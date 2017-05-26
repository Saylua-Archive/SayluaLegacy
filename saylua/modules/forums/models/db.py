from saylua import db, app


r_board_categories = db.Table('r_board_categories',
    db.Column('board_id', db.Integer, db.ForeignKey('forum_boards.id')),
    db.Column('category_id', db.Integer, db.ForeignKey('forum_board_categories.id'))
)


class BoardCategory(db.Model):
    """Forum Board Categories.
    Many to Many relationship with `Board`.
    """

    __tablename__ = "forum_board_categories"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(128))

    order = db.Column(db.Integer)

    boards = db.relationship("Board",
        secondary=r_board_categories,
        back_populates="categories",
        lazy='dynamic'
    )

    def get_boards(self, user=None):
        query = self.boards
        if not (user and user.has_moderation_access()):
            query = query.filter(Board.moderators_only == False)
        return query.order_by(Board.order.asc()).all()


class Board(db.Model):
    """Forum Boards. Container for threads.
    Many to Many relationship with `BoardCategory`.
    """

    __tablename__ = 'forum_boards'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(256))
    canon_name = db.Column(db.String(256), unique=True)
    description = db.Column(db.Text())

    moderators_only = db.Column(db.Boolean(), default=False)

    order = db.Column(db.Integer)

    categories = db.relationship("BoardCategory",
        secondary=r_board_categories,
        back_populates="boards"
    )

    threads = db.relationship("ForumThread", back_populates="board")

    def url(self):
        return "/forums/board/" + self.canon_name + "/"

    def is_new(self):
        return self.canon_name == app.config.get('NEWS_BOARD_CANON_NAME')

    def latest_post(self):
        return (
            db.session.query(ForumPost)
            .join(ForumThread, ForumPost.thread)
            .filter(ForumThread.board_id == self.id)
            .order_by(ForumPost.date_modified.desc())
            .first()
        )

    @classmethod
    def by_canon_name(cls, name):
        return db.session.query(cls).filter(cls.canon_name == name.lower()).one_or_none()


class ForumThread(db.Model):
    """Forum Threads.
    Many to One relationship with `Board`.
    """

    __tablename__ = "forum_threads"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(256))
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    author = db.relationship("User")

    date_created = db.Column(db.DateTime, server_default=db.func.now())
    date_modified = db.Column(db.DateTime, server_default=db.func.now())

    is_pinned = db.Column(db.Boolean(), default=False)
    is_locked = db.Column(db.Boolean(), default=False)

    board_id = db.Column(db.Integer, db.ForeignKey('forum_boards.id'))
    board = db.relationship("Board", back_populates="threads")

    posts = db.relationship("ForumPost", back_populates="thread", lazy='dynamic')

    def url(self):
        return "/forums/thread/" + str(self.id) + "/"

    def first_post(self):
        return self.posts.order_by(ForumPost.date_created.asc()).first()

    def reply_count(self):
        return (
            db.session.query(ForumPost)
            .filter(ForumPost.thread_id == self.id)
            .count() - 1
        )

    def latest_post(self):
        return (
            db.session.query(ForumPost)
            .filter(ForumPost.thread_id == self.id)
            .order_by(ForumPost.date_modified.desc())
            .first()
        )


class ForumPost(db.Model):
    """Forum Thread Posts.
    Many to One relationship with `ForumThread`.
    """

    __tablename__ = "forum_thread_posts"

    id = db.Column(db.Integer, primary_key=True)
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    author = db.relationship("User")

    body = db.Column(db.Text())

    date_created = db.Column(db.DateTime, server_default=db.func.now())
    date_modified = db.Column(db.DateTime, server_default=db.func.now())

    thread_id = db.Column(db.Integer, db.ForeignKey('forum_threads.id'))
    thread = db.relationship("ForumThread", back_populates="posts")
