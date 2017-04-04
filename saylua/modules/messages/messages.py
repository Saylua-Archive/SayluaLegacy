from flask import render_template, redirect, flash, request, g
from google.appengine.ext import ndb
import flask_sqlalchemy
from saylua import db

from saylua.wrappers import login_required
from saylua.utils import pluralize, get_from_request
from .models.db import Conversation, ConversationUser, Message
from saylua.models.user import User

from forms import ConversationForm, ConversationReplyForm, recipient_check
from saylua.utils.form import flash_errors


# The main page where the user views all of their messages.
@login_required
def messages_main():
    conversations = (
        db.session.query(ConversationUser)
        .filter(ConversationUser.user_id == g.user.id)
        .order_by(ConversationUser.last_updated.desc())
        .order_by(ConversationUser.unread)
        .all()
    )
    return render_template('messages/all.html', messages=conversations)


# The submit action for the user to update their messages.
@login_required
def messages_main_post():
    user_message_ids = request.form.getlist('user_conversation_id')
    keys = []
    for m_id in user_message_ids:
        if not m_id:
            flash('You are attempting to edit an invalid message!', 'error')
            return redirect('/messages/', code=302)
        keys.append(m_id)

    user_messages = ndb.get_multi(keys)
    for m in user_messages:
        if not m:
            flash('You are attempting to edit a message which does not exist!', 'error')
            return redirect('/messages/', code=302)
        if m.user_id != g.user.id:
            flash('You do not have permission to edit these messages!', 'error')
            return redirect('/messages/', code=302)

        m.is_deleted = 'delete' in request.form
        m.unread = 'read' not in request.form

    if 'delete' in request.form:
        ndb.put_multi(user_messages)
        flash(pluralize(len(keys), 'message') + ' deleted. ')
    elif 'read' in request.form:
        ndb.put_multi(user_messages)
        flash(pluralize(len(keys), 'message') + ' marked as read. ')
    return redirect('/messages/', code=302)


# The page for a user to write new messages.
@login_required
def messages_write_new():
    form = ConversationForm(request.form)
    form.recipient.data = get_from_request(request, 'recipient', args_key='to')
    form.title.data = get_from_request(request, 'title')
    form.text.data = get_from_request(request, 'text')

    if request.method == 'POST' and form.validate():
        to = recipient_check.user.id
        new_id = start_conversation(g.user.id, to, form.title.data, form.text.data)
        return redirect('/conversation/' + str(new_id) + '/', code=302)

    flash_errors(form)
    return render_template('messages/write.html', form=form)


# This route just marks a conversationuser as read and then redirects the user to the
# conversation they were looking to read. We make it a separate route so that the
# main "looking at a message" route doesn't have to bother with looking up
# the user's message metadata.
@login_required
def messages_read(key):
    try:
        found_conversation = db.session.query(ConversationUser).get((key, g.user.id))
        found_conversation.unread = False
        db.session.commit()
        return redirect('/conversation/' + str(key) + '/', code=302)
    except(flask_sqlalchemy.orm.exc.NoResultFound):
        return render_template('messages/invalid.html')


# The page to view a specific conversation.
@login_required
def messages_view_conversation(key):
    found_conversation = db.session.query(ConversationUser).get((key, g.user.id))
    if not found_conversation:
        return render_template('messages/invalid.html')

    form = ConversationReplyForm()
    form.text.data = get_from_request(request, 'text')
    if request.method == 'POST' and form.validate():
        result = reply_conversation(key, g.user.id, form.text.data)
        if result:
            flash('You have replied to the message!')
            return redirect('/conversation/' + str(key) + '/', code=302)
        else:
            flash('Message reply failed for an unexpected reason.', 'error')
    flash_errors(form)
    members = (
        db.session.query(User)
        .join(ConversationUser)
        .filter(ConversationUser.conversation_id == key)
        .all()
    )
    messages = (
        db.session.query(Message)
        .filter(Message.conversation_id == key)
        .all()
    )
    return render_template('messages/view.html', conversation=found_conversation,
        members=members, conversation_messages=messages, form=form)


def start_conversation(sender_id, recipient_ids, title, text):
    new_conversation = Conversation()
    db.session.add(new_conversation)
    db.session.flush()
    first_message = Message(conversation_id=new_conversation.id, author_id=sender_id, text=text)
    db.session.add(first_message)
    send_member = ConversationUser(conversation_id=new_conversation.id,
            user_id=sender_id, title=title, unread=False)
    db.session.add(send_member)
    if isinstance(recipient_ids, (int, long)): # noqa
        recipient_ids = [recipient_ids]
    recipient_ids = set(recipient_ids) # Remove duplicates
    if sender_id in recipient_ids:
        recipient_ids.remove(sender_id)
    for recip_id in recipient_ids:
        db.session.add(ConversationUser(conversation_id=new_conversation.id,
                user_id=recip_id, title=title, unread=True))
    db.session.commit()
    return new_conversation.id


def reply_conversation(conversation_id, author_id, text):
    new_message = Message(conversation_id=conversation_id, author_id=author_id, text=text)
    db.session.add(new_message)
    conversation_users = (
        db.session.query(ConversationUser)
        .filter(ConversationUser.conversation_id == conversation_id)
        .all()
    )
    for conversation_user in conversation_users:
        conversation_user.last_updated = db.func.now()
        if conversation_user.user_id != author_id:
            conversation_user.unread = True
        db.session.add(conversation_user)
    db.session.commit()
    return True
