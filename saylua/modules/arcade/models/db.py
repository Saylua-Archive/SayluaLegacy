from saylua import db


# Enum type thing, raises a ValueError if not found
def Game(game):
    games = ["blocks"]
    try:
        return games[game]
    except TypeError:
        return games.index(game)


class Highscore(db.Model):
    __tablename__ = "highscores"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    user = db.relationship("User")

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
    user = db.relationship("User")

    game_id = db.Column(db.Integer, nullable=False)
    score = db.Column(db.Integer)
    time = db.Column(db.DateTime, server_default=db.func.now())

    # Note: Game logs are differently formatted per type of game.
    game_log = db.Column(db.Text)

    @classmethod
    def record_score(cls, user_id, game_id, score):
        new_record = cls(user_id=user_id, game_id=game_id, score=score)
        db.session.add(new_record)
        db.session.commit()

    @classmethod
    def get_user_highscore(cls, user_id, game_id):
        return (
            db.session.query(cls)
            .filter(cls.user_id == user_id)
            .filter(cls.game_id == game_id)
            .order_by(cls.score.desc())
            .limit(1)
            .all()
        )

    @classmethod
    def get_highscores(cls, game_id, count=10):
        return (
            db.session.query(cls)
            .filter(cls.game_id == game_id)
            .order_by(cls.score.desc())
            .limit(count)
            .all()
        )
