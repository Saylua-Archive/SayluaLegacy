from google.appengine.ext import ndb
from google.appengine.ext.ndb import msgprop

from protorpc import messages


class Game(messages.Enum):
    LINE_BLOCKS = 1


# This is a model for storing scores that users get in arcade games.
# This also doubles as a log of rewards that users received from games.
class GameScore(ndb.Model):
    user_key = ndb.KeyProperty()
    game_id = msgprop.EnumProperty(Game, required=True)
    score = ndb.IntegerProperty()
    time = ndb.DateTimeProperty(auto_now_add=True)

    @classmethod
    def record_score(cls, user_key, game_id, score):
        score = cls(user_key=user_key, game_id=game_id, score=score)
        return score.put()

    @classmethod
    def get_user_highscore(cls, user_key, game_id, score):
        return cls.query(cls.game_id == game_id, cls.user_key == user_key).order(
            -cls.score).fetch(limit=1)

    @classmethod
    def get_highscores(cls, game_id, count=10):
        return cls.query(cls.game_id == game_id).order(-cls.score).fetch(
            limit=count)
