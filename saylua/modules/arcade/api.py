from saylua.wrappers import login_required
from flask import g, request
from models.db import Game, GameScore
from saylua.models.user import User

import json


# Send a score to the API.
# TODO: Implement login_required that returns error for API call, rather than
# redirecting to /login.
@login_required
def api_send_score(game):
    try:
        game = Game(game)
    except TypeError:
        return json.dumps(dict(error='Invalid game!')), 400
    finally:
        if game == Game.LINE_BLOCKS:
            data = request.get_json()
            GameScore.record_score(g.user.key, game, data['score'])
            cc, ss = User.update_currency(g.user.key, cc=data['score'])
            return json.dumps(dict(cloud_coins=cc, star_shards=ss))
    return json.dumps(dict(error='Bad request.')), 400
