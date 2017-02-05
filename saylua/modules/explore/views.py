from saylua.wrappers import login_required
from .dungeons import Dungeon

from flask import render_template, flash
from random import randint

import json


@login_required
def home():
    return render_template("map.html")


@login_required
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
