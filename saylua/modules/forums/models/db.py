from saylua import db, app

from saylua.utils import truncate, canonize

from saylua.modules.messages.models.db import Notification


class BoardCategory(db.Model):
    """Forum Board Categories.
    Many to Many relationship with `Board`.
    """

    __tablename__ = "forum_board_categories"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(256))
    canon_name = db.Column(db.String(256), unique=True)

    order = db.Column(db.Integer, default=1)

    boards = db.relationship("Board",
        back_populates="category",
        lazy='dynamic'
    )

    def url(self):
        return '/forums/#' + self.canon_name

    def get_boards(self, user=None):
        query = self.boards
        if not (user and user.has_moderation_access()):
            query = query.filter(Board.moderators_only == False)
        return query.order_by(Board.order.asc()).all()

    @classmethod
    def get_categories(cls):
        return db.session.query(cls).order_by(cls.order.asc()).all()

    @classmethod
    def by_canon_name(cls, name):
        return db.session.query(cls).filter(cls.canon_name == name.lower()).one_or_none()


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

    category_id = db.Column(db.Integer, db.ForeignKey('forum_board_categories.id'))
    category = db.relationship("BoardCategory",
        back_populates="boards"
    )

    threads = db.relationship("ForumThread", back_populates="board")

    def url(self):
        return "/forums/board/" + self.canon_name + "/"

    def is_news(self):
        return self.canon_name == app.config.get('NEWS_BOARD_CANON_NAME')

    def can_post(self, user):
        result = user and user.has_communication_access()
        if self.is_news():
            result = result and user.has_admin_access()
        return result

    def latest_post(self):
        return (
            db.session.query(ForumPost)
            .join(ForumThread, ForumPost.thread)
            .filter(ForumThread.board_id == self.id)
            .order_by(ForumPost.id.desc())
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
    date_modified = db.Column(db.DateTime, onupdate=db.func.now())

    is_pinned = db.Column(db.Boolean(), default=False)
    is_locked = db.Column(db.Boolean(), default=False)

    board_id = db.Column(db.Integer, db.ForeignKey('forum_boards.id'))
    board = db.relationship("Board", back_populates="threads")

    posts = db.relationship("ForumPost", back_populates="thread", lazy='dynamic')

    subscribers = db.relationship("User", secondary='forum_thread_subscriptions',
        lazy='dynamic')

    def notify_subscribers(self, post):
        for user in self.subscribers:
            if user.id == post.author_id:
                continue
            Notification.send(user.id, 'Someone has made a new post in the thread: ' + self.title,
                post.url())

    def url(self):
        return "/forums/thread/" + str(self.id) + "-" + canonize(truncate(self.title, 40)) + "/"

    def subscription(self, user):
        return user and db.session.query(ForumSubscription).get((self.id, user.id))

    def can_post(self, user):
        result = user and user.has_communication_access()
        if self.is_locked:
            result = result and user.has_moderation_access()
        return result

    def can_edit(self, user):
        return user and user.has_communication_access() and (user.id == self.author.id or
            user.has_moderation_access())

    def first_post(self):
        return self.posts.order_by(ForumPost.id.asc()).first()

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
            .order_by(ForumPost.id.desc())
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
    date_modified = db.Column(db.DateTime, onupdate=db.func.now())

    thread_id = db.Column(db.Integer, db.ForeignKey('forum_threads.id'))
    thread = db.relationship("ForumThread", back_populates="posts")

    def url(self):
        index = (
            db.session.query(ForumPost)
            .filter(ForumPost.thread_id == self.thread_id)
            .filter(ForumPost.id < self.id)
            .count()
        )
        page = (index // app.config.get('POSTS_PER_PAGE')) + 1
        return str(self.thread.url()) + str(page) + "/" + self.anchor()

    def anchor(self):
        return "#post-" + str(self.id)

    def can_edit(self, user):
        return user and user.has_communication_access() and (user.id == self.author.id or
            user.has_moderation_access())


class ForumSubscription(db.Model):
    __tablename__ = "forum_thread_subscriptions"

    thread_id = db.Column(db.Integer, db.ForeignKey('forum_threads.id'), primary_key=True)
    thread = db.relationship("ForumThread")

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)
    user = db.relationship("User")
