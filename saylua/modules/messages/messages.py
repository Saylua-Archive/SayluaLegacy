from flask import render_template, redirect, flash, request, g
from google.appengine.ext import ndb

from saylua import app, login_required
from saylua.utils import make_ndb_key, pluralize, get_from_request
from saylua.models.conversation import UserConversation, Conversation

from forms import ConversationForm, ConversationReplyForm, recipient_check
from saylua.utils.form import flash_errors


# The main page where the user views all of their messages.
@app.route('/messages/')
@login_required
def messages_main():
    messages = UserConversation.query(UserConversation.user_key == g.user.key,
        UserConversation.is_deleted == False).order(
        UserConversation.is_read, -UserConversation.time).fetch()
    if not messages:
        messages = []
    return render_template('messages/all.html', viewed_messages=messages)


# The submit action for the user to update their messages.
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


# The page for a user to write new messages.
@app.route('/messages/write/', methods=['GET', 'POST'])
@login_required
def messages_write_new():
    form = ConversationForm(request.form)
    form.recipient.data = get_from_request(request, 'recipient', args_key='to')
    form.title.data = get_from_request(request, 'title')
    form.text.data = get_from_request(request, 'text')

    if request.method == 'POST' and form.validate():
        to = recipient_check.user.key
        key = Conversation.start(g.user.key, to, form.title.data, form.text.data)
        return redirect('/conversation/' + key.urlsafe() + '/', code=302)

    flash_errors(form)
    return render_template('messages/write.html', form=form)


# This route just marks a message as read and then redirects the user to the
# message they were looking to read. We make it a separate route so that the
# main "looking at a message" route doesn't have to bother with looking up
# the user's message metadata.
@app.route('/conversation_read/<key>/')
@login_required
def messages_read(key):
    conversation_key = make_ndb_key(key)
    if conversation_key:
        conversation = UserConversation.query(UserConversation.user_key == g.user.key,
            UserConversation.conversation_key == conversation_key).get()
        if conversation:
            conversation.is_read = True
            conversation.put()
            return redirect('/conversation/' + conversation_key.urlsafe() + '/', code=302)
    return render_template('messages/invalid.html')


# The page to view a specific conversation.
@app.route('/conversation/<key>/', methods=['GET', 'POST'])
@login_required
def messages_view_conversation(key):
    key = make_ndb_key(key)
    conversation = get_conversation_if_valid(key)
    if not conversation:
        return render_template('messages/invalid.html')

    form = ConversationReplyForm()
    form.text.data = get_from_request(request, 'text')
    if request.method == 'POST' and form.validate():
        result = Conversation.reply(key, g.user.key, form.text.data)
        if result:
            flash('You have replied to the message!')
            return redirect('/conversation/' + key.urlsafe() + '/', code=302)
        else:
            flash('Message reply failed for an unexpected reason.', 'error')
    flash_errors(form)
    return render_template('messages/view.html', conversation=conversation,
        form=form)


# Non-route functions.
def get_conversation_if_valid(key):
    if key:
        conversation = Conversation.get_by_id(key.id())
        if conversation:
            # Check that the user has permission to view the message
            if g.user.key in conversation.user_keys:
                return conversation
    return None
