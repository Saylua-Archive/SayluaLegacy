from bcryptmaster import bcrypt

from saylua import db
from saylua.utils import random_token

from .bank import BankAccount
from .moderation import BanTypes
from .codes import EmailConfirmationCode, PasswordResetCode

from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import validates

import datetime


# An exception thrown if an operation would make a user's currency negative
class InvalidCurrencyException(Exception):
    pass


class User(db.Model):
    """The greatest User model of all time.
    """

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)

    active_username = db.Column(db.String(80), unique=True)

    last_username_change = db.Column(db.DateTime, server_default=db.func.now())
    username_objects = db.relationship("Username", back_populates="user")

    last_action = db.Column(db.DateTime, server_default=db.func.now())
    date_joined = db.Column(db.DateTime, server_default=db.func.now())

    # Email, Password
    email = db.Column(db.String(120), unique=True)
    email_confirmed = db.Column(db.Boolean, default=False)
    password_hash = db.Column(db.String(200))

    # Permissions.
    can_moderate = db.Column(db.Boolean, default=False)
    can_admin = db.Column(db.Boolean, default=False)

    title_id = db.Column(db.Integer, db.ForeignKey("titles.id"))
    title = db.relationship("Title", foreign_keys=[title_id])
    titles = db.relationship("Title",
        secondary="r_user_titles",
        back_populates="users"
    )

    post_count = db.Column(db.Integer, default=0)

    # Active Companion
    companion_id = db.Column(db.Integer, db.ForeignKey("pets.id"))
    companion = db.relationship("Pet", foreign_keys=[companion_id])
    pets = db.relationship("Pet", primaryjoin='Pet.guardian_id == User.id',
        back_populates="guardian", lazy='dynamic')

    # Ban Status
    ban_id = db.Column(db.Integer, db.ForeignKey("ban_logs.id"))
    ban = db.relationship("BanLog", foreign_keys=[ban_id])

    # Currency
    star_shards = db.Column(db.Integer, default=0)
    cloud_coins = db.Column(db.Integer, default=0)
    bank_account = db.relationship("BankAccount", uselist=False, back_populates="user")

    # Misc profile stuff
    gender = db.Column(db.String(100), default="")
    pronouns = db.Column(db.String(200), default="")
    bio = db.Column(db.String(1000), default="Hello, world")
    status = db.Column(db.String(15), default="")

    # Settings
    side_id = db.Column(db.Integer, default=0)
    theme_id = db.Column(db.Integer, default=0)
    notified_on_pings = db.Column(db.Boolean, default=True)
    autosubscribe_threads = db.Column(db.Boolean, default=True)
    autosubscribe_posts = db.Column(db.Boolean, default=False)

    # Used to track linear progress. ie: 0-5 are levels of the tutorial.
    story_level = db.Column(db.Integer, default=0)

    def __repr__(self):
        return '<User %r>' % self.name

    @hybrid_property
    def name(self):
        return self.active_username

    @name.setter
    def set_name(self, name):
        self.active_username = name

    @property
    def usernames(self):
        return [u.name for u in self.username_objects]

    def avatar_url(self):
        # Until we implement human avatars for real...
        return '/static/img/avatar/base.png'

    def url(self):
        return "/user/" + self.name.lower() + "/"

    def title_class(self):
        if self.is_banned():
            return 'title-banned'
        elif self.is_muted():
            return 'title-muted'
        elif self.title:
            return self.title.css_class()
        return 'title-user'

    def story_route(self):
        if self.story_level == 0:
            return 'general.intro_side'
        elif self.story_level == 1:
            return 'general.intro_companion'
        elif self.story_level == 2:
            return 'general.intro_avatar'
        return None

    def side_name(self):
        if self.side_id == 0:
            return 'Sayleus'
        elif self.side_id == 1:
            return 'Luaria'
        return None

    def is_banned(self):
        ban = self.ban
        return ban and ban.ban_type == BanTypes.BAN and ban.active()

    def is_muted(self):
        ban = self.ban
        return ban and ban.ban_type == BanTypes.MUTE and ban.active()

    def has_communication_access(self):
        return self.email_confirmed and not self.is_muted() and not self.is_banned()

    def has_moderation_access(self):
        return self.can_moderate

    def has_admin_access(self):
        return self.can_admin

    def make_email_confirmation_code(self):
        code = EmailConfirmationCode(self.id, self.email)
        db.session.merge(code)
        db.session.commit()
        return code

    def make_password_reset_code(self):
        code = PasswordResetCode(self.id)
        db.session.merge(code)
        db.session.commit()
        return code

    @validates('email')
    def validate_email(self, key, address):
        return address.lower()

    @validates('cloud_coins')
    def validate_cloud_coins(self, key, cc):
        if cc < 0:
            raise InvalidCurrencyException("Currency cannot be negative!")
        return cc

    @validates('star_shards')
    def validate_star_shards(self, key, ss):
        if ss < 0:
            raise InvalidCurrencyException("Currency cannot be negative!")
        return ss

    @classmethod
    def by_username(cls, username):
        return (
            db.session.query(cls)
            .join(Username, cls.id == Username.user_id)
            .filter(Username.name == username.lower())
            .one_or_none()
        )

    @classmethod
    def from_email(cls, email):
        return db.session.query(cls).filter(cls.email == email.lower()).one_or_none()

    @classmethod
    def hash_password(cls, password, salt=None):
        if not salt:
            salt = bcrypt.gensalt()
        return bcrypt.hashpw(password, salt)

    @classmethod
    def check_password(cls, user, password):
        return cls.hash_password(password, user.password_hash) == user.password_hash

    @classmethod
    def transfer_currency(cls, from_id, to_id, cc=0, ss=0):
        from_user = db.session.query(User).get(from_id)
        to_user = db.session.query(User).get(to_id)
        if cc > from_user.cloud_coins or ss > from_user.star_shards:
            raise InvalidCurrencyException('Insufficient funds!')
        from_user.star_shards -= ss
        from_user.cloud_coins -= cc
        to_user.star_shards += ss
        to_user.cloud_coins += cc

    def __init__(self, username, *args, **kwargs):
        self.active_username = username
        Username.create(username, self)

        self.bank_account = BankAccount()

        super(User, self).__init__(*args, **kwargs)


class Username(db.Model):
    """Represents the username of a user.

    Multiple names can be tied to one user, but only one of
    them can be active and nested within the user class.

    Many to one relationship with `User`.
    """

    __tablename__ = "usernames"

    # The unique username stored in lowercase.
    name = db.Column(db.String(80), primary_key=True)

    # A record of the name as the user typed it.
    case_name = db.Column(db.String(80))

    # The linked user
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    user = db.relationship("User", back_populates="username_objects")

    # Account for case sensitivity in username uniqueness.
    @classmethod
    def create(cls, name, user):
        return cls(name=name.lower(), case_name=name, user=user)

    # Get username object from username.
    @classmethod
    def get(cls, name):
        return db.session.query(cls).get(name.lower())


class LoginSession(db.Model):
    __tablename__ = "sessions"

    id = db.Column(db.String(256), primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), primary_key=True)
    user = db.relationship("User")

    expires = db.Column(db.DateTime)

    def __init__(self, user_id, expires):
        self.id = random_token(128)
        self.user_id = user_id
        self.expires = expires

    @property
    def active(self):
        return (self.expires > datetime.datetime.now())
