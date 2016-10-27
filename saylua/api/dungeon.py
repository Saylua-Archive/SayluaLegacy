from saylua import app, login_required
from saylua.models.dungeon import Dungeon
from saylua.utils.terrain import Terrain, TileGrid, EntityContainer
from saylua.utils.terrain.helpers import diff

from flask import (url_for, session, abort, request, g)

from random import shuffle
import json


def generate_dungeon():
  # Grab a random dungeon type
  dungeon_types = list(Terrain.terrains.keys())
  shuffle(dungeon_types)
  dungeon_name = dungeon_types[0]
  dungeon_api = Terrain.terrains[dungeon_name]

  # Stick with default option set for now.
  default_options = dungeon_api.get('default_options')

  # Create our map. Yeah, this syntax is weird.
  grid = dungeon_api['generate'](default_options)

  # Iterate the suggested amount of times.
  # Modifies grid in-place.
  for i in xrange(default_options.get('iterations', 1)):
    dungeon_api['iterate'](default_options, grid)

  # Create our entity layer. (And hide tiles)
  entities = dungeon_api['populate'](default_options, grid)

  return dungeon_name, grid, entities


@app.route('/api/explore/get/', methods=['POST'])
@login_required
def api_dungeon_request():
  # Acquire our dungeon
  dungeon = Dungeon.query(Dungeon.user_key == g.user_key).fetch()

  if dungeon and False:
    dungeon = dungeon[0]
  else:
    # Initialize the user's very first dungeon.
    name, grid, entities = generate_dungeon()
    dungeon = Dungeon.create(
      user_key=g.user_key,
      name=name,
      tile_layer=grid.to_string(),
      entity_layer=entities.to_string()
    ).get()

  # Get our essentials
  dungeon_api = Terrain.terrains[dungeon.name]
  grid = TileGrid.TileGrid.from_string(dungeon.tile_layer)
  entities = EntityContainer.EntityContainer.from_string(dungeon.entity_layer)

  tile_set = dungeon_api.get("tile_set")
  entity_set = dungeon_api.get("entity_set")

  player = entities.get_player()
  player_position = (player['location']['x'], player['location']['y'])

  # Store visible entities prior to calculating visibility for diffing reasons.
  grid_pre = grid.get_visible()
  entities_pre = grid.get_visible()

  # Calculate the visible and non-visible tiles and entities.
  # We are defaulting to a radius of 8 for now.
  grid.calculate_visible(player_position, 8)
  entities.calculate_visible(grid)

  # If this is an 'initial' request, dump all data and stop here.
  # It was originally planned that entity data would only be sent once seen,
  # this is not necessary at the moment, so the entire set will always be sent.
  if request.form.get('initial') == True:
    return json.dumps({
      "tileSet": tile_set,
      "entitySet": entity_set,
      "tileLayer": grid.get_visible(),
      "entityLayer": entities.get_visible()
    })

  # Send a diff instead.
  else:
    return json.dumps({
      "tileSet": [],
      "entitySet": [],
      "tileLayer": grid.get_visible(), #diff(grid_pre, grid.get_visible(), 'tile'),
      "entityLayer": entities.get_visible() #diff(entities_pre, entities.get_visible(), 'id')
    })


@app.route('/api/explore/move/', methods=['POST'])
def api_map_move():
    if not (request.form and request.form["x"] and request.form["y"]):
        return json.dumps({'Error': 'Bad API Usage. '}), 400

    result = {}

    return json.dumps(result)
