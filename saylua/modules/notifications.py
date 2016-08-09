from saylua import app
from flask import (render_template, redirect, make_response,
                   url_for, flash, session, abort, request)
from saylua.models.notification import Notification

@app.route('/notifications/')
def notifications_main():
    return render_template("notifications/all.html")

@app.route('/notifications/', methods=['POST'])
def notifications_main_post():
    return render_template("notifications/all.html")

@app.route('/notifications/<int:key>/')
def notifications_follow(key):
    notification = Notification.get_by_id(key)
    if notification:
        return redirect(notification.link, code=302)
    return render_template("notifications/invalid.html")
