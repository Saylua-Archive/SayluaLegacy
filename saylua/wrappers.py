from flask import redirect as _redirect, url_for, render_template, g, flash

from saylua.utils import is_devserver
from functools import wraps

import json

DEFAULT_LOGIN_ERROR = 'You must be logged in to use this feature.'


def devserver_only(f):
    """Prevents non developer instances from viewing a route.

    Usage: `@devserver_only`
    """

    @wraps(f)
    def decorated_function(*args, **kwargs):
        if is_devserver():
            return f(*args, **kwargs)
        return render_template('404.html'), 404

    return decorated_function


def login_required(f, redirect='users.login', error=DEFAULT_LOGIN_ERROR):
    """Redirects non-logged in users to a specified location.

    Usage: `@login_required`, `@login_required(redirect=<url>)`
    """

    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not g.logged_in:
            flash(error)
            return _redirect(url_for(redirect))
        return f(*args, **kwargs)

    return decorated_function


# Based on http://www.artima.com/weblogs/viewpost.jsp?thread=240845
class login_required_with_args(object):
    def __init__(self, redirect='users.login', error=DEFAULT_LOGIN_ERROR):
        self.redirect = redirect
        self.error = error

    def __call__(self, f):
        return login_required(f, self.redirect, self.error)


def communication_access_required(f, redirect='home.main'):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not g.logged_in:
            flash(DEFAULT_LOGIN_ERROR)
            return _redirect(url_for('users.login'))

        if g.user.is_muted():
            flash("You can't use this feature while muted.")
            return _redirect(url_for(redirect))

        if not g.user.email_confirmed:
            flash("Please confirm your email before using this feature.")
            return _redirect(url_for(redirect))

        return f(*args, **kwargs)

    return decorated_function


def moderation_access_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not g.logged_in:
            flash(DEFAULT_LOGIN_ERROR)
            return _redirect(url_for('users.login'))

        if not g.user.has_moderation_access():
            return render_template('403.html'), 403

        return f(*args, **kwargs)

    return decorated_function


def admin_access_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not g.logged_in:
            flash(DEFAULT_LOGIN_ERROR)
            return _redirect(url_for('users.login'))

        if not g.user.has_admin_access():
            return render_template('403.html'), 403

        return f(*args, **kwargs)

    return decorated_function


# Same as login_required but returns a 400 response for API endpoints.
def api_login_required(f, error='You must be logged in to use this feature.'):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not g.logged_in:
            return json.dumps(dict(error=error)), 401
        return f(*args, **kwargs)

    return decorated_function
