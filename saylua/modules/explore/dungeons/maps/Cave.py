from meta.EntityContainer import EntityContainer
from meta.APIWrapper import APIWrapper
from meta.TileGrid import TileGrid
from meta import default_entities

from random import shuffle

# Cave Map -> Dungeon Terrain Type
# ===================================================
# In the future, have this dungeon make itself more dangerous over time.
# Continuously generating low level slimes that grow in size (And therefore strength)
# as the number of turns increases.
# The goal on Cave dungeons should be to find the exit as fast as possible or suffer
# the consequences.

## Todo:
## - Above mentioned lateral difficulty.
## - Closed areas must be eliminated programmatically or pathed to. Preferably inlined into populate()
## - Portal should be placed a minimum distance from the player, with a weighted bias towards corners.


def generate(options):
    # Reasons
    width, height = options.get("size")

    # Prepare empty map
    grid = TileGrid(width=width, height=height, default_tile='0x00')

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


def finalize(options, grid):
    for x, y, cell in grid.iterate():
        # Ensure all edge cells are walls.
        if x in [0, (grid.width - 1)] or y in [0, (grid.height - 1)]:
            grid.set((x, y), '0x01')

    # Add cell-neighbor information. Fairly expensive, but it only runs once.
    # 0000: top, right, bottom, left.
    ordinals = ""

    # Top
    if y == 0:
        ordinals += "1"
    else:
        neighbor_north = grid.get((x, y - 1))

        if neighbor_north.get('tile') == '0x01':
            ordinals += "1"
        else:
            ordinals += "0"

    # Right
    if x == (grid.width - 1):
        ordinals += "1"
    else:
        neighbor_east = grid.get((x + 1, y))

        if neighbor_east.get('tile') == '0x01':
            ordinals += "1"
        else:
            ordinals += "0"

    # Bottom
    if y == (grid.height - 1):
        ordinals += "1"
    else:
        neighbor_south = grid.get((x, y + 1))

        if neighbor_south.get('tile') == '0x01':
            ordinals += "1"
        else:
            ordinals += "0"

    # Left
    if x == 0:
        ordinals += "1"
    else:
        neighbor_west = grid.get((x - 1, y))

        if neighbor_west.get('tile') == '0x01':
            ordinals += "1"
        else:
            ordinals += "0"

    grid.cell_map[y][x]['meta']['ordinals'] = ordinals


def populate(options, grid):
    # Find a non-wall location and insert the player.
    non_walls = grid.find(lambda x: x['tile'] == '0x00')
    shuffle(non_walls)

    player_location = non_walls[0]
    portal_location = non_walls[1]

    entities = EntityContainer()
    entities.add(parent='0x1000', location=player_location)
    entities.add(parent='0x1001', location=portal_location)

    # Add placeholder slimes in 5% of remaining space.
    non_walls = non_walls[2:]
    number_of_slimes = int(round(len(non_walls) * 0.05))

    for i in range(number_of_slimes):
        entities.add(parent='0x2000', location=non_walls[i])

    return entities

API = APIWrapper({
    "generate": generate,
    "finalize": finalize,
    "iterate": iterate,
    "populate": populate,
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
            'slug': 'tile_cave_ground',
            'type': 'ground',
            'meta': {}
        },
        {
            'id': '0x01',
            'description': 'The mottled walls of this cavern somehow manage to feel both rough and slimy simultaneously. You also feel a slow, heartbeat like thrumming. Curious.',
            'slug': 'tile_cave_wall',
            'type': 'wall',
            'meta': {}
        }
    ],
    "entity_set": default_entities
})
