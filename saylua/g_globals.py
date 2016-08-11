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
        found = LoginSession.query(LoginSession.user_key == user_key,
                LoginSession.session_key == session_key).get()
    if found == None:
        g.logged_in = False
        g.user = None
        return None
    key = ndb.Key(urlsafe=user_key)
    founduser = key.get()
    g.logged_in = True
    g.user = founduser
