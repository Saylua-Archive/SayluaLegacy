DEBUG = True
SESSION_LIMIT = 5
COOKIE_DURATION = 30
MAIN_URL_ROOT = 'https://saylua.com'

# Form fields
MIN_USERNAME_LENGTH = 3
MAX_USERNAME_LENGTH = 15

MIN_PASSWORD_LENGTH = 5
MAX_PASSWORD_LENGTH = 200

MAX_USER_STATUS_LENGTH = 15

# Number of minutes from a user's last action for them to be counted as online.
USERS_ONLINE_RANGE = 15
LAST_ACTION_OFFSET = 5

# Maximum number of usernames that a single user can own.
MAX_USERNAMES = 10

# Regexes and stuff.
EMAIL_REGEX = '(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)'
USERNAME_REGEX = '^[A-Za-z0-9+~._-]+$'
CANON_NAME_REGEX = '^[a-z0-9+_]+$'

# Registration settings.
REGISTRATION_DISABLED = False
INVITE_ONLY = True

# Disable the Flask-SQLAlchemy event system for now as it's kinda buggy and not needed.
SQLALCHEMY_TRACK_MODIFICATIONS = False

# Email settings
AUTOSEND_EMAIL = 'Saylua <noreply@mg.saylua.com>'

# The canon name used to pull in news.
NEWS_BOARD_CANON_NAME = 'news'
