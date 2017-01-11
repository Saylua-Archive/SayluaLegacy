from google.appengine.ext import ndb
from google.appengine.ext.ndb import msgprop

from protorpc import messages


class Game(messages.Enum):
    LINE_BLOCKS = 1


# This is a model for storing scores that users get in arcade games.
# This also doubles as a long of rewards that users received from games.
class GameScore(ndb.Model):
    user_key = ndb.KeyProperty()
    game_id = msgprop.EnumProperty(Game, required=True)
    score = ndb.IntegerProperty()
    time = ndb.DateTimeProperty(auto_now_add=True)

    @classmethod
    def record_score(cls, user_key, game_id, score):
        score = cls(user_key=user_key, game_id=game_id, score=score)
        return score.put()
