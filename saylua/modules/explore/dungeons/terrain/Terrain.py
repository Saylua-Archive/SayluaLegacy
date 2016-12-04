from . import Cave

import json


# This belongs in it's own file, probably as a class.
# It is here for now while we iterate.
def mutate(grid, entities, mutation):
  mutation = json.loads(mutation)
  event_log = None

  if mutation.get('action') == 'move':
    direction = mutation.get('data')

    player = entities.get_player()
    p_x = player['location']['x']
    p_y = player['location']['y']

    g_x = p_x
    g_y = p_y

    # Surely, there's a better way to do this?
    if direction == 'up':
      g_y = p_y - 1
    elif direction == 'down':
      g_y = p_y + 1
    elif direction == 'left':
      g_x = p_x - 1
    elif direction == 'right':
      g_x = p_x + 1

    # Figure out where we're going
    goal_cell = grid.get((g_x, g_y))

    # Determine if we can go there, theoretically
    if not goal_cell:
      return grid, entities, event_log

    # Determine if we can go there, physically
    obstacle_types = ['wall']

    matching_tile = filter(lambda tile: tile.get('id') == goal_cell['tile'], tiles)
    matching_tile = list(matching_tile)[0]

    is_obstacle = matching_tile['type'] in obstacle_types

    if is_obstacle:
      return grid, entities, event_log

    # If we've gotten this far, we can finally move the player.
    player['location']['x'] = g_x
    player['location']['y'] = g_y
    entities.update_entity(player)

    event_log = "OH MY SWEET GODS ABOVE"

  return grid, entities, event_log


terrains = {
  "cave": Cave.API
}


# There should really be a REAL tile lookup service,
# with static methods for determining things like
# whether or not a tile is an obstacle.
tiles = Cave.API.get('tile_set')
