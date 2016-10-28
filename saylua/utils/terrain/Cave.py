from saylua.utils.terrain import default_entities
from random import shuffle

# Cave -> Required by Terrain
# ===================================================
# In the future, have this dungeon make itself more dangerous over time.
# Continuously generating low level slimes that grow in size (And therefore strength) as the number of turns increases.
# The goal on Cave dungeons should be to find the exit as fast as possible or suffer the consequences.

## Todo:
## - Above mentioned lateral difficulty.
## - Closed areas must be eliminated programmatically or pathed to. Preferably inlined into populate()
## - Portal should be placed a minimum distance from the player, with a weighted bias towards corners.


def generate(options):
  # Prevent circular import issues
  from saylua.utils.terrain import TileGrid

  # Reasons
  width, height = options.get("size")

  # Prepare empty map
  grid = TileGrid.TileGrid(width=width, height=height, default_tile='0x00')

  # Seed with cells. Enforce an exact fill percentage, with no overlap.
  cells_to_fill = int(round(options.get("fill_percentage") * (width * height)))
  cells = [i for i, e in enumerate(range(width * height))]
  shuffle(cells)

  cells = cells[:cells_to_fill]

  for i in cells:
    # Find the X and Y coordinates from a linear integer
    # We do this by using whole number division and then modulus.
    y = i // width
    x = i % width

    grid.set((x, y), '0x01')

  return grid


def iterate(options, grid):
  from itertools import chain

  # A cell with N adjacent floors (including itself) becomes a floor.
  # Otherwise, it becomes a wall. The goal is to average cell
  # distribution uniformly.
  for x, y, cell in grid.iterate():
    # Grab neighbor subset, flatten
    neighbors = grid.get((x - 1, y - 1), (x + 1, y + 1))
    neighbors = list(chain.from_iterable(neighbors))
    floor_count = sum(1 for n in neighbors if n.get('tile') == '0x00')

    if floor_count >= options.get("minimum_neighbors"):
      grid.set((x, y), '0x00')
    else:
      grid.set((x, y), '0x01')

  return True


def populate(options, grid):
  # Prevent circular import issues
  from saylua.utils.terrain import EntityContainer

  # Find a non-wall location and insert the player.
  non_walls = grid.find(lambda x: x['tile'] == '0x00')
  shuffle(non_walls)

  # An additional step must be added to ensure that the player
  # and portal are not inserted into a non-pathable location.
  # See: "The Dungeon Update" commit notes for details
  player_location = non_walls[0]
  portal_location = non_walls[1]

  entities = EntityContainer.EntityContainer()
  entities.add(parent='0x1000', location=player_location)
  entities.add(parent='0x1001', location=portal_location)

  # Add placeholder slimes in 5% of remaining space.
  non_walls = non_walls[2:]
  number_of_slimes = int(round(len(non_walls) * 0.05))

  for i in range(number_of_slimes):
    entities.add(parent='0x2000', location=non_walls[i])

  return entities

API = {
  "generate": generate,
  "iterate":  iterate,
  "populate":  populate,
  "default_options": {
    "fill_percentage": 0.63,
    "minimum_neighbors": 4,
    "iterations": 4,
    "size": [80, 50]
  },
  "tile_set": [
    {
      'id': '0x00',
      'description': 'Ugh, gross. What did you just step in?',
      'type': 'ground',
      'meta': {}
    },
    {
      'id': '0x01',
      'description': 'The mottled walls of this cavern somehow manage to feel both rough and slimy simultaneously. You also feel a slow, heartbeat like thrumming. Curious.',
      'type': 'wall',
      'meta': {}
    }
  ],
  "entity_set": default_entities
}
