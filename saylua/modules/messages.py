from saylua import app, login_required
from saylua.utils import make_ndb_key, pluralize
from flask import (render_template, redirect, make_response,
                   url_for, flash, session, abort, request, g)
from saylua.models.messages import ConversationUser, Conversation

@app.route('/messages/')
@login_required
def messages_main():
    messages = ConversationUser.query(ConversationUser.user_key==g.user.key).order(
        ConversationUser.is_read, -ConversationUser.time).fetch()
    if not messages:
        messages = []
    return render_template('messages/all.html', viewed_messages=messages)

@app.route('/conversation_read/<key>/')
@login_required
def messages_read(key):
    conversation_key = make_ndb_key(key)
    if conversation_key:
        conversation = ConversationUser.query(ConversationUser.user_key==g.user.key,
            ConversationUser.conversation_key==conversation_key).get()
        if conversation:
            conversation.is_read = True
            conversation.put()
            return redirect('/conversation/' + conversation_key.urlsafe() + '/', code=302)
    return render_template('messages/invalid.html')



@app.route('/conversation/<key>/')
@login_required
def messages_view(key):
    key = make_ndb_key(key)
    conversation = getConversationIfValid(key)
    if conversation:
        return render_template('messages/view.html', conversation=conversation)
    return render_template('messages/invalid.html')

@app.route('/conversation/<key>/', methods=['POST'])
@login_required
def messages_reply(key):
    key = make_ndb_key(key)
    conversation = getConversationIfValid(key)
    if conversation:
        text = request.form['text']
        if text and len(text) >= 2:
            result = Conversation.reply(key, g.user.key, text)
            if result:
                flash('You have replied to the message!')
            else:
                flash('Message reply failed for an unexpected reason.', 'error')
        else:
            flash('Your reply must be at least 2 characters!', 'error')
    return redirect('/conversation/' + key.urlsafe() + '/', code=302)

# Non-route functions

def getConversationIfValid(key):
    if key:
        conversation = Conversation.get_by_id(key.id())
        if conversation:
            # Check that the user has permission to view the message
            if not g.user.key in conversation.user_keys:
                return conversation
    return None
