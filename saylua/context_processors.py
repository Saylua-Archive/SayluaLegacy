from saylua import app
from dateutil import tz
import datetime
from flask import request
from saylua.models.user import LoginSession, User

@app.context_processor
def inject_time():
    time = datetime.datetime.now()
    from_zone = tz.gettz('UTC')
    to_zone = tz.gettz('America/New_York')
    time = time.replace(tzinfo = from_zone)
    time = time.astimezone(to_zone)
    time = time.strftime("%I:%M:%S %p SST")
    return dict(saylua_time=time)
