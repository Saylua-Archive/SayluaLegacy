from saylua import app
from flask import (render_template, redirect, make_response,
                   url_for, flash, session, abort, request)

@app.route('/messages/')
def messages_main():
    return render_template("messages/all.html")

@app.route('/conversation/<key>/')
def messages_view(key):
    return render_template("messages/view.html")
