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


def check_login(error=DEFAULT_LOGIN_ERROR, redirect='users.login'):
    if not g.logged_in:
        flash(error)
        return _redirect(url_for(redirect))

    if g.user.is_banned():
        flash("You can't use this feature while banned.", 'error')
        return _redirect('/banned')

    return None


class login_required(object):
    def __init__(self, redirect='users.login', error=DEFAULT_LOGIN_ERROR):
        self.redirect = redirect
        self.error = error

    def __call__(self, f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            response = check_login(self.error, self.redirect)
            if response:
                return response
            return f(*args, **kwargs)

        return decorated_function


def communication_access_required(f, redirect='home.main'):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        response = check_login()
        if response:
            return response

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
        response = check_login()
        if response:
            return response

        if not g.user.has_moderation_access():
            return render_template('403.html'), 403

        return f(*args, **kwargs)

    return decorated_function


def admin_access_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        response = check_login()
        if response:
            return response

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
