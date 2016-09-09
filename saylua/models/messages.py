from google.appengine.ext import ndb
from saylua.models.user import User
from saylua.utils import make_ndb_key

import datetime

# TODO: Make things transactional

# StructuredProperty for Conversation
class ConversationMessage(ndb.Model):
    user_key = ndb.KeyProperty()
    text = ndb.StringProperty()
    time = ndb.DateTimeProperty(auto_now_add=True)

class Conversation(ndb.Model):
    title = ndb.StringProperty()
    messages = ndb.StructuredProperty(ConversationMessage, repeated=True)
    user_keys = ndb.KeyProperty(repeated=True)

    @classmethod
    def start(cls, sender_key, recipient_key, title, text):
        # Set the first message of the conversation
        conversation_messages = [ConversationMessage(user_key=sender_key, text=text)]

        conversation = cls(title=title, messages=conversation_messages,
            user_keys=[sender_key, recipient_key])

        conversation_key = conversation.put()

        # Add all people in the conversation (ConversationUser)
        if recipient_key != sender_key:
            sender = ConversationUser(conversation_key=conversation_key,
                user_key=sender_key, recipient_keys=[recipient_key], title=title,
                is_read=True, is_first=True)
            sender.put()

        recipient = ConversationUser(conversation_key=conversation_key,
            user_key=recipient_key, title=title, recipient_keys=[sender_key])
        recipient.put()

        return conversation_key

    @classmethod
    def reply(cls, conversation_key, user_key, text):
        time = datetime.datetime.now()

        # Update the user statuses
        sender = ConversationUser.query(
            ConversationUser.conversation_key==conversation_key,
            ConversationUser.user_key==user_key).get()

        # Check that the user has permission to reply to this conversation
        if not sender:
            return None

        sender.time = time
        sender.is_replied = True
        sender.is_read = True
        sender.is_deleted = False

        # Update recipient status
        for recipient_key in sender.recipient_keys:
            recipient = ConversationUser.query(
                ConversationUser.conversation_key==conversation_key,
                ConversationUser.user_key==recipient_key).get()
            # This should always exist, but if not something is wrong with the data.
            if recipient:
                recipient.time = time
                recipient.is_first = False
                recipient.is_replied = False
                recipient.is_read = False
                recipient.is_deleted = False
                recipient.put()

        # Add the new message
        conversation = Conversation.get_by_id(conversation_key.id())
        conversation_message = ConversationMessage(user_key=user_key, text=text)
        conversation.messages.append(conversation_message)

        result = conversation.put()
        sender.put()

        return result

# Child
class ConversationUser(ndb.Model):
    user_key = ndb.KeyProperty(indexed=True)
    recipient_keys = ndb.KeyProperty(indexed=True, repeated=True)
    conversation_key = ndb.KeyProperty(indexed=True)
    title = ndb.StringProperty()

    # Status precendence order: Deleted > Unread > Sent > Replied > Read
    is_first = ndb.BooleanProperty(default=False)
    is_replied = ndb.BooleanProperty(default=False)
    is_read = ndb.BooleanProperty(default=False, indexed=True)
    is_deleted = ndb.BooleanProperty(default=False, indexed=True)

    time = ndb.DateTimeProperty(indexed=True, auto_now_add=True)
