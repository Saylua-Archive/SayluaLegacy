from saylua.wrappers import login_required, devserver_only

from .dungeons import Dungeon
from .models.db import DungeonEntity, DungeonTile

from flask import render_template

import json


@login_required()
def home():
    return render_template("map.html")


@login_required()
@devserver_only
def api_entity_list():
    entities = [x.to_dict() for x in DungeonEntity.query.all()]

    return json.dumps({
        "result": entities
    })


@login_required()
@devserver_only
def api_tile_list():
    tiles = [x.to_dict() for x in DungeonTile.query.all()]

    return json.dumps({
        "result": tiles
    })


@login_required()
def generate_dungeon():
    # Acquire our dungeon
    dungeon = Dungeon.Dungeon()

    return json.dumps({
        "dungeonInfo": dungeon.get_info(),
        "tileSet": dungeon.tile_set,
        "entitySet": dungeon.entity_set,
        "tileLayer": dungeon.grid.render(),
        "entityLayer": dungeon.entities.render()
    })
