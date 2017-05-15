from flask import redirect as _redirect, url_for, render_template, g
from saylua.utils import is_devserver
from functools import wraps

import json


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


def login_required(f, redirect='users.login'):
    """Redirects non-logged in users to a specified location.

    Usage: `@login_required`, `@login_required(redirect=<url>)`
    """

    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not g.logged_in:
            return _redirect(url_for(redirect))
        return f(*args, **kwargs)

    return decorated_function


def email_confirmation_required(f, redirect='home.main'):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not g.logged_in:
            return _redirect(url_for('users.login'))

        if not g.user.email_confirmed:
            return _redirect(url_for(redirect))

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


def admin_access_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not g.user.get_role() or not g.user.get_role().can_access_admin:
            return render_template('403.html'), 403

        return f(*args, **kwargs)

    return decorated_function
