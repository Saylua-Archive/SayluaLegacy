from google.appengine.ext import ndb
import user

class Notification(ndb.Model):
    user_key = ndb.KeyProperty(indexed=True)
    time = ndb.DateTimeProperty(auto_now_add=True)
    text = ndb.StringProperty()
    link = ndb.StringProperty()
    is_read = ndb.BooleanProperty(default=False, indexed=True)
    count = ndb.IntegerProperty(default=1)

    @classmethod
    def send(cls, user_key, text, link):
        notification = cls.query(cls.user_key==user_key,
            cls.text==text, cls.link==link, cls.is_read==False).get()
        if not notification:
            notification = cls(user_key=user_key, text=text, link=link)
        else:
            notification.count += 1
        return notification.put()
