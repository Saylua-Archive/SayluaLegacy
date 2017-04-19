from saylua.wrappers import api_login_required
from flask import g, request
from models.db import Game, GameLog
from saylua.models.user import User

import json


# Send a score to the API.
@api_login_required
def api_send_score(game):
    try:
        gameName = Game(game)
    except IndexError:
        return json.dumps(dict(error='Invalid game!')), 400
    finally:
        if gameName == "LINE_BLOCKS":
            # TODO sanity check the game log and other variables sent to catch
            # low hanging fruit attempts at cheating.
            data = request.get_json()
            GameLog.record_score(g.user.id, game, data['score'])
            cc, ss = User.update_currency(g.user.id, cc=data['score'])
            return json.dumps(dict(cloud_coins=cc, star_shards=ss))
    return json.dumps(dict(error='Bad request.')), 400
