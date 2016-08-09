from saylua import app
from dateutil import tz
import datetime
from flask import request
from saylua.models.user_model import LoginSession, User

@app.context_processor
def inject_time():
    time = datetime.datetime.now()
    from_zone = tz.gettz('UTC')
    to_zone = tz.gettz('America/New_York')
    time = time.replace(tzinfo = from_zone)
    time = time.astimezone(to_zone)
    time = time.strftime("%I:%M:%S %p SST")
    return dict(saylua_time=time)

@app.context_processor
def inject_user():
    username = request.cookies.get('username')
    session_key = request.cookies.get('session_key')
    found = None
    if username and session_key:
        found = LoginSession.query(LoginSession.username == username,
                LoginSession.session_key == session_key).get()
    if found == None:
        return dict(logged_in=False)
    founduser = User.query(User.username == username).get()
    return dict(logged_in=True,
        username=founduser.username,
        display_name=founduser.display_name)
