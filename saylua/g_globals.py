from saylua import app
from flask import request, g
from saylua.models.user import LoginSession, User

@app.before_request
def load_user():
    username = request.cookies.get('username')
    session_key = request.cookies.get('session_key')
    found = None
    if username and session_key:
        found = LoginSession.query(LoginSession.username == username,
                LoginSession.session_key == session_key).get()
    if found == None:
        g.logged_in = False
        g.user = None
        return None
    founduser = User.query(User.username == username).get()
    g.logged_in = True
    g.user = founduser
