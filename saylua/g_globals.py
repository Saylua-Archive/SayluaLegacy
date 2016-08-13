from saylua import app
from flask import request, g
from google.appengine.ext import ndb
from saylua.models.user import LoginSession, User
from saylua.utils import make_ndb_key

@app.before_request
def load_user():
    if request.script_root == '/static':
        return
    user_key = request.cookies.get('user_key')
    session_key = request.cookies.get('session_key')
    found = None
    if user_key and session_key:
        s_key = make_ndb_key(session_key)
        u_key = make_ndb_key(user_key)

        if not s_key or not u_key:
            g.logged_in = False
            g.user = None
            return None

        found = s_key.get()
        if found.user_key != user_key:
            found = None
    if not found:
        g.logged_in = False
        g.user = None
        return None
    founduser = u_key.get()
    g.logged_in = True
    g.user = founduser
