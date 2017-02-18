from saylua import app, db
from saylua.models.user import LoginSession
from flask import request, g
import datetime


@app.before_request
def load_user():
    # Make sure not to run function for static files
    if request.script_root == '/static':
        return

    # Load user
    session_id = request.cookies.get('session_id')

    if session_id:
        session = (
            db.session.query(LoginSession)
            .filter(LoginSession.id == session_id)
            .first()
        )

        if session:
            user = session.get_user()

            if user and session.active:
                g.logged_in = True
                g.user = user

                # Update user's last_action timestamp if it's been at least
                # LAST_ACTION_OFFSET minutes
                current = datetime.datetime.now()
                mins_ago = current - datetime.timedelta(
                    minutes=app.config['LAST_ACTION_OFFSET'])

                if g.user and g.user.last_action < mins_ago:
                    g.user.last_action = current
                    db.session.commit()

                return

    g.logged_in = False
    g.user = None
    return None
