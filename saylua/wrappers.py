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


def login_required_response(error=DEFAULT_LOGIN_ERROR, redirect='users.login'):
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
            response = login_required_response(self.error, self.redirect)
            if response:
                return response
            return f(*args, **kwargs)

        return decorated_function


class communication_access_required(object):
    def __init__(self, redirect='home.main'):
        self.redirect = redirect

    def __call__(self, f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            response = login_required_response()
            if response:
                return response

            if g.user.is_muted():
                flash("You can't use this feature while muted.")
                return _redirect(url_for(self.redirect))

            if not g.user.email_confirmed:
                flash("Please confirm your email before using this feature.")
                return _redirect(url_for(self.redirect))

            return f(*args, **kwargs)

        return decorated_function


class moderation_access_required(object):
    def __init__(self, redirect=None):
        self.redirect = redirect

    def __call__(self, f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            response = login_required_response()
            if response:
                return response

            if not g.user.has_moderation_access():
                if self.redirect:
                    flash("You don't have permission to use this feature.")
                    return _redirect(url_for(self.redirect))
                return render_template('403.html'), 403

            return f(*args, **kwargs)

        return decorated_function


class admin_access_required(object):
    def __init__(self, redirect=None):
        self.redirect = redirect

    def __call__(self, f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            response = login_required_response()
            if response:
                return response
            if not g.user.has_admin_access():
                if self.redirect:
                    flash("You don't have permission to use this feature.")
                    return _redirect(url_for(self.redirect))
                return render_template('403.html'), 403

            return f(*args, **kwargs)

        return decorated_function


# Same as login_required but returns a 400 response for API endpoints.
class api_login_required(object):
    def __init__(self, error=DEFAULT_LOGIN_ERROR):
        self.error = error

    def __call__(self, f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if login_required_response():
                return json.dumps(dict(error=self.error)), 401
            return f(*args, **kwargs)

        return decorated_function
