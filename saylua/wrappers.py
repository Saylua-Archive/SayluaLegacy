from flask import redirect as _redirect, url_for, render_template, g
from functools import wraps


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


def admin_access_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not g.logged_in:
            return _redirect(url_for('users.login'))

        if not g.user.get_role() or not g.user.get_role().can_access_admin:
            return render_template('403.html'), 403

        return f(*args, **kwargs)

    return decorated_function
