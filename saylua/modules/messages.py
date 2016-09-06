from saylua import app, login_required
from flask import (render_template, redirect, make_response,
                   url_for, flash, session, abort, request, g)
from saylua.models.messages import ConversationUser

@app.route('/messages/')
@login_required
def messages_main():
    messages = ConversationUser.query(ConversationUser.user_key==g.user.key).order(
        ConversationUser.is_read, -ConversationUser.time).fetch()
    if not messages:
        messages = []

    return render_template('messages/all.html', viewed_messages=messages)

@app.route('/conversation/<key>/')
@login_required
def messages_view(key):
    return render_template('messages/view.html')
