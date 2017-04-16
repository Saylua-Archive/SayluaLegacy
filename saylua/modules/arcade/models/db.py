from saylua import db
from google.appengine.ext.ndb import msgprop

from protorpc import messages


class Game(messages.Enum):
    LINE_BLOCKS = 1


class Highscore(db.Model):
    __tablename__ = "highscores"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    game_log_id = db.Column(db.Integer, db.ForeignKey('gamelogs.id'))
    game_id = db.Column(db.Integer, nullable=False)
    score = db.Column(db.Integer)

    # Highscores are monthly. For an all-time highscore, year and month are set
    # to zero.
    year = db.Column(db.Integer)
    month = db.Column(db.Integer)


# Stores a log of a player's gameplay including score.
class GameLog(db.Model):
    __tablename__ = "gamelogs"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    game_id = db.Column(db.Integer, nullable=False)
    score = db.Column(db.Integer)
    time = db.Column(db.DateTime(timezone=True), server_default=db.func.now())

    # Note: Game logs are differently formatted per type of game.
    game_log = ndb.JsonProperty(indexed=False)

    @classmethod
    def record_score(cls, user_id, game_id, score):
        score = cls(user_id=user_id, game_id=game_id, score=score)
        return score.put()

    @classmethod
    def get_user_highscore(cls, user_id, game_id, score):
        return cls.query(cls.game_id == game_id, cls.user_id == user_id).order(
            -cls.score).fetch(limit=1)

    @classmethod
    def get_highscores(cls, game_id, count=10):
        return cls.query(cls.game_id == game_id).order(-cls.score).fetch(
            limit=count)
