from saylua import app
from flask import request, g
from google.appengine.ext import ndb
from saylua.models.user import LoginSession, User

@app.before_request
def load_user():
    user_key = request.cookies.get('user_key')
    session_key = request.cookies.get('session_key')
    found = None
    if user_key and session_key:
        try:
            s_key = ndb.Key(urlsafe=session_key)
            u_key = ndb.Key(urlsafe=user_key)
        except Exception:
            g.logged_in = False
            g.user = None
            return None
        found = s_key.get()
        if found.user_key != user_key:
            found = None
    if found == None:
        g.logged_in = False
        g.user = None
        return None
    founduser = u_key.get()
    g.logged_in = True
    g.user = founduser
