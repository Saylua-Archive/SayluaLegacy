from google.appengine.ext import ndb

from protorpc import messages


class Game(messages.Enum):
    LINE_BLOCKS = 1


# This is a model for storing scores that users get in arcade games.
# This also doubles as a long of rewards that users received from games.
class GameScore(ndb.Model):
    user_key = ndb.KeyProperty()
    game_id = ndb.EnumProperty(Game, required=True)
    score = ndb.IntegerProperty()
    time = ndb.DateTimeProperty(auto_now_add=True)
