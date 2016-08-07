from saylua import app
from flask import (render_template, redirect, make_response,
                   url_for, flash, session, abort, request)

@app.route('/notifications/')
def notifications_main():
    return render_template("notifications/all.html")
