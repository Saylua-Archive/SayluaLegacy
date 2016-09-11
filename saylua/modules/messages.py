from flask import (render_template, redirect, make_response,
                   url_for, flash, session, abort, request, g)
from google.appengine.ext import ndb

from saylua import app, login_required
from saylua.utils import make_ndb_key, pluralize, get_from_request
from saylua.models.messages import UserConversation, Conversation
from saylua.models.user import User
from saylua.utils.validation import FieldValidator

@app.route('/messages/')
@login_required
def messages_main():
    messages = UserConversation.query(UserConversation.user_key==g.user.key,
        UserConversation.is_deleted==False).order(
        UserConversation.is_read, -UserConversation.time).fetch()
    if not messages:
        messages = []
    return render_template('messages/all.html', viewed_messages=messages)

@app.route('/messages/', methods=['POST'])
@login_required
def messages_main_post():
    user_message_ids = request.form.getlist('user_conversation_id')
    keys = []
    for m_id in user_message_ids:
        m_id = make_ndb_key(m_id)
        if not m_id:
            flash('You are attempting to edit an invalid message!', 'error')
            return redirect('/messages/', code=302)
        keys.append(m_id)

    user_messages = ndb.get_multi(keys)
    for m in user_messages:
        if not m:
            flash('You are attempting to edit a message which does not exist!', 'error')
            return redirect('/messages/', code=302)
        if m.user_key != g.user.key:
            flash('You do not have permission to edit these messages!', 'error')
            return redirect('/messages/', code=302)

        m.is_deleted = 'delete' in request.form
        m.is_read = 'read' in request.form

    if 'delete' in request.form:
        ndb.put_multi(user_messages)
        flash(pluralize(len(keys), 'message') + ' deleted. ')
    elif 'read' in request.form:
        ndb.put_multi(user_messages)
        flash(pluralize(len(keys), 'message') + ' marked as read. ')
    return redirect('/messages/', code=302)

@app.route('/messages/write/', methods=['GET', 'POST'])
@login_required
def messages_write_new():
    recipient = get_from_request(request, 'recipient', args_key='to')
    title = get_from_request(request, 'title')
    text = get_from_request(request, 'text')

    if request.method == 'POST':
        recipientValidator = (FieldValidator('recipient', recipient).required().min(2))
        titleValidator = (FieldValidator('title', title).required().min(2))
        textValidator = (FieldValidator('text', text).required().min(3))
        recipientValidator.flash()
        titleValidator.flash()
        textValidator.flash()

        if recipientValidator and titleValidator and textValidator:
            to = User.key_by_username(recipient)
            if to:
                key = Conversation.start(g.user.key, to, title, text)
                return redirect('/conversation/' + key.urlsafe() + '/', code=302)
            else:
                flash(recipient + ' is not a valid username! ', 'error')

    return render_template('messages/write.html', recipient=recipient,
        title=title, text=text)

@app.route('/conversation_read/<key>/')
@login_required
def messages_read(key):
    conversation_key = make_ndb_key(key)
    if conversation_key:
        conversation = UserConversation.query(UserConversation.user_key==g.user.key,
            UserConversation.conversation_key==conversation_key).get()
        if conversation:
            conversation.is_read = True
            conversation.put()
            return redirect('/conversation/' + conversation_key.urlsafe() + '/', code=302)
    return render_template('messages/invalid.html')

@app.route('/conversation/<key>/', methods=['GET', 'POST'])
@login_required
def messages_view(key):
    key = make_ndb_key(key)
    conversation = get_conversation_if_valid(key)
    if conversation:
        text = get_from_request(request, 'text')
        if request.method == 'POST':
            textValidator = (FieldValidator('text', text).required().min(2))
            textValidator.flash()
            if textValidator.valid:
                result = Conversation.reply(key, g.user.key, text)
                if result:
                    flash('You have replied to the message!')
                    return redirect('/conversation/' + key.urlsafe() + '/', code=302)
                else:
                    flash('Message reply failed for an unexpected reason.', 'error')
        return render_template('messages/view.html', conversation=conversation, reply_text=text)
    return render_template('messages/invalid.html')

# Non-route functions

def get_conversation_if_valid(key):
    if key:
        conversation = Conversation.get_by_id(key.id())
        if conversation:
            # Check that the user has permission to view the message
            if g.user.key in conversation.user_keys:
                return conversation
    return None
