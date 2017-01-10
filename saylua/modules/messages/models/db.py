from google.appengine.ext import ndb

import datetime


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

        # Add all people in the conversation (UserConversation)
        if recipient_key != sender_key:
            sender = UserConversation(conversation_key=conversation_key,
                user_key=sender_key, recipient_keys=[recipient_key], title=title,
                is_read=True, is_first=True)
            sender.put()

        recipient = UserConversation(conversation_key=conversation_key,
            user_key=recipient_key, title=title, recipient_keys=[sender_key])
        recipient.put()

        return conversation_key

    @classmethod
    def reply(cls, conversation_key, user_key, text):
        time = datetime.datetime.now()

        # Update the user statuses
        sender = UserConversation.query(
            UserConversation.conversation_key == conversation_key,
            UserConversation.user_key == user_key).get()

        # Check that the user has permission to reply to this conversation
        if not sender:
            return None

        sender.time = time
        sender.is_replied = True
        sender.is_read = True
        sender.is_deleted = False

        # Update recipient status
        for recipient_key in sender.recipient_keys:
            recipient = UserConversation.query(
                UserConversation.conversation_key == conversation_key,
                UserConversation.user_key == recipient_key).get()
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
class UserConversation(ndb.Model):
    user_key = ndb.KeyProperty()
    recipient_keys = ndb.KeyProperty(repeated=True)
    conversation_key = ndb.KeyProperty()
    title = ndb.StringProperty()

    # Status precendence order: Deleted > Unread > Sent > Replied > Read
    is_first = ndb.BooleanProperty(default=False)
    is_replied = ndb.BooleanProperty(default=False)
    is_read = ndb.BooleanProperty(default=False)
    is_deleted = ndb.BooleanProperty(default=False)

    time = ndb.DateTimeProperty(auto_now_add=True)


class Notification(ndb.Model):
    user_key = ndb.KeyProperty()
    time = ndb.DateTimeProperty(auto_now_add=True)
    text = ndb.StringProperty(indexed=False)
    link = ndb.StringProperty(indexed=False)
    is_read = ndb.BooleanProperty(default=False)
    count = ndb.IntegerProperty(default=1)

    @classmethod
    def send(cls, user_key, text, link):
        notification = cls.query(cls.user_key == user_key,
            cls.text == text, cls.link == link, cls.is_read == False).get()
        if not notification:
            notification = cls(user_key=user_key, text=text, link=link)
        else:
            notification.count += 1
        return notification.put()
