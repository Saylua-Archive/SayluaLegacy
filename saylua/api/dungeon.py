from saylua import app
from saylua.models.dungeon import ExploreMap

from flask import (url_for, session, abort, request)

import json

@app.route('/api/explore/map/')
def api_map_generation():
    # TODO: Make sure to authorize player for viewing map
    explore_map = ExploreMap(7, 7)
    return explore_map.json()

@app.route('/api/explore/move/', methods=['POST'])
def api_map_move():
    if not (request.form and request.form["x"] and request.form["y"]):
        return json.dumps({'Error' : 'Bad API Usage. '}), 400

    result = {}

    return json.dumps(result)
