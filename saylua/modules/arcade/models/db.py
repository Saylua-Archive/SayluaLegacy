from google.appengine.ext import ndb
from google.appengine.ext.ndb import msgprop

from protorpc import messages


class Game(messages.Enum):
    LINE_BLOCKS = 1


class Highscore(ndb.Model):
    user_key = ndb.KeyProperty()
    game_log_key = ndb.KeyProperty()
    game_id = msgprop.EnumProperty(Game, required=True)
    score = ndb.IntegerProperty()

    # Highscores are monthly. For an all-time highscore, year and month are set
    # to zero.
    year = ndb.IntegerProperty()
    month = ndb.IntegerProperty()


# Stores a log of a player's gameplay including score.
class GameLog(ndb.Model):
    user_key = ndb.KeyProperty()
    game_id = msgprop.EnumProperty(Game, required=True)
    score = ndb.IntegerProperty()
    time = ndb.DateTimeProperty(auto_now_add=True)

    # Note: Game logs are differently formatted per type of game.
    game_log = ndb.JsonProperty(indexed=False)

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
