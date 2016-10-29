from saylua import app, login_required
from google.appengine.api import memcache

from saylua.utils.terrain import Terrain
from saylua.utils.terrain.TileGrid import TileGrid
from saylua.utils.terrain.EntityContainer import EntityContainer
from saylua.utils.terrain.helpers import diff

from saylua.utils import saylua_time

from flask import (url_for, session, abort, request, g)

from datetime import datetime
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

  # Create our map. Yeah, this syntax is ultra weird.
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
  dungeon = memcache.get('dungeon-%s' % g.user_key.urlsafe())

  if not dungeon:
    # Initialize the user's very first dungeon.
    name, grid, entities = generate_dungeon()
    dungeon = Dungeon()
    dungeon.name = name
    dungeon.tile_layer = grid.to_string()
    dungeon.entity_layer = entities.to_string()

  # Get our essentials
  dungeon_api = Terrain.terrains[dungeon.name]
  grid = TileGrid.from_string(dungeon.tile_layer)
  entities = EntityContainer.from_string(dungeon.entity_layer)

  tile_set = dungeon_api.get("tile_set")
  entity_set = dungeon_api.get("entity_set")

  # Mutate, as necessary.
  if request.form.get('mutation'):
    grid, entities = Terrain.mutate(grid, entities, request.form.get('mutation'))

  # Calculate the visible and non-visible tiles and entities.
  # We are defaulting to a radius of 8 for now.
  player = entities.get_player()
  player_position = (player['location']['x'], player['location']['y'])

  grid.calculate_visible(player_position, 8)
  entities.calculate_visible(grid)

  # Store changes
  dungeon.tile_layer = grid.to_string()
  dungeon.entity_layer = entities.to_string()
  dungeon.last_accessed = datetime.now()
  memcache.set('dungeon-%s' % g.user_key.urlsafe(), dungeon)

  # If this is an 'initial' request, dump all data and stop here.
  # It was originally planned that entity data would only be sent once seen,
  # this is not necessary while testing, so the entire set will always be sent.
  if request.form.get('initial') == True or True:
    return json.dumps({
      "tileSet": tile_set,
      "entitySet": entity_set,
      "tileLayer": grid.get_visible(),
      "entityLayer": entities.get_visible()
    })

class Dungeon:
    pass
