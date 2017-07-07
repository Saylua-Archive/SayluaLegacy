from saylua import db

from saylua.wrappers import api_login_required
from flask import g, request
from models.db import Game, GameLog

from saylua.utils import int_or_none

import json


# Send a score to the API.
@api_login_required()
def api_send_score(game_id):
    try:
        gameName = Game(game_id)
    except IndexError:
        return json.dumps(dict(error='Invalid game!')), 400
    finally:
        if gameName == "blocks":
            # TODO sanity check the game log and other variables sent to catch
            # low hanging fruit attempts at cheating.
            data = request.get_json()
            score = int_or_none(data.get('score')) or 0
            GameLog.record_score(g.user.id, game_id, score)
            g.user.cloud_coins += score
            db.session.commit()
            return json.dumps(dict(cloud_coins=g.user.cloud_coins, star_shards=g.user.star_shards))
    return json.dumps(dict(error='Bad request.')), 400
