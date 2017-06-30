from saylua import app, db
from saylua.modules.users.models.db import LoginSession
from flask import request, g

import datetime


@app.before_request
def load_user():
    # Make sure not to run function for static files
    if request.url_rule and '/static/' in request.url_rule.rule:
        return

    # Load user
    session_id = request.cookies.get('session_id')
    user_id = request.cookies.get('user_id')

    if session_id and user_id:
        try:
            user_id = int(user_id)
        except ValueError:
            return

        session = db.session.query(LoginSession).get((session_id, user_id))

        if session:
            user = session.user

            if user and session.active:
                g.logged_in = True
                g.user = user

                # Update user's last_action timestamp if it's been at least
                # LAST_ACTION_OFFSET minutes.
                current = datetime.datetime.now()
                mins_ago = current - datetime.timedelta(
                    minutes=app.config['LAST_ACTION_OFFSET'])

                if g.user and g.user.last_action < mins_ago:
                    g.user.last_action = current
                    db.session.commit()

                return

    g.logged_in = False
    g.user = None
    return
