from saylua.utils.terrain import Terrain
from saylua.utils.terrain import helpers

import cPickle, copy

# TileGrid -> Required by dungeon(s)
# Utility class for the terrain generators.
# ===================================================
# Note:
# A tile with an unset meta.visibility value is treated as unseen.
# A tile with a set but falsey meta.visibility value is treated as seen but hidden.
#
# Sample 1x3 map:
# [
#   {
#     'tile': '0x00',
#     'meta': {
#       'elevation': 1,
#       'visible': True
#     }
#   },
#   {
#     'tile': '0x05',
#     'meta': {
#       'message': "THE FLOOR IS LAVA!"
#       'elevation': 0
#     }
#   },
#   {
#     'tile': '0x00',
#     'meta': {
#       'elevation': 1,
#       'visible': False
#     }
#   }
# ]

class TileGrid():
  def __init__(self, width, height, cell_map=None):
    self.width = width
    self.height = height

    if cell_map:
      self.cell_map = cell_map

    else:
      self.cell_map = []

      # Populate with empty cells
      for row in xrange(height):
        self.cell_map.append([{'tile': None, 'meta': {}}] * width)

      # Generates lists that all refer to the same
      # point in memory. Not useful.
      # [[0] * width] * height

  def get(self, a, b=None):
    # Default to returning a single cell,
    # return an array subset if a second argument is provided.
    a_x, a_y = a

    if b is None:
      return self.cell_map[y][x]

    else:
      sub_map = []
      b_x, b_y = b

      height = b_y - a_y
      width = b_x - a_x

      for offset in xrange(height + 1):
        y = a_y + offset

        if y < self.height:
          cells = self.cell_map[y][a_x : a_x + (width + 1)]
          sub_map.append(cells)

      return sub_map

  def set(self, coords, value, meta=None):
    x, y = coords

    try:
      self.cell_map[y][x]['tile'] = value

      if meta and (type(meta) == dict):
        self.cell_map[y][x]['meta'] = meta

      return self.cell_map

    except IndexError:
      print("Tried filling ({}, {}), and failed. You really messed up.".format(x, y))
      raise

  def find(self, search_function):
    # Returns a list of tupled cell locations that satisfy <search_function>
    results = []

    for x, y, cell in self.iterate(static=False):
      if search_function(cell):
        results.append((x, y))

    return results

  def iterate(self, static=True):
    # Generator that yields cells. Exists for performance / niceness reasons.
    # Works from a copy so that iterators can edit the object's grid in-place.
    working_set = None

    if static:
      working_set = copy.deepcopy(self.cell_map)
    else:
      working_set = self.cell_map

    for y in xrange(self.height):
      for x in xrange(self.width):
        yield (x, y, working_set[y][x])

  def fill_circle(self, center, radius, filler, meta=None):
    # Fill circles from the center, with radius of N.
    c_x, c_y = center
    for x, y, cell in self.iterate(static=False):
      # Calculate box shaped FOV
      within_range_x = (c_x - radius) <= x <= (c_x + radius)
      within_range_y = (c_y - radius) <= y <= (c_y + radius)

      if within_range_x and within_range_y:
        # Calculate circle shaped FOV, fill cells
        if round(helpers.distance((x, y), center)) <= radius:
          self.cell_map[y][x]['tile'] = filler

          if meta:
            self.cell_map[y][x]['meta'] = meta

  def fill_rectangle(self, a, b, filler, meta=None):
    # Fill from top left corner to bottom right corner.
    # Will automatically ignore out of bounds coordinates.

    a_x, a_y = a
    b_x, b_y = b

    height = b_y - a_y
    width = b_x - a_x

    for offset in xrange(height + 1):
      # Determine row
      y = a_y + offset

      if y < self.height:
        # Make sure that we're not inserting more cells than are being selected.
        new_cells = self.cell_map[y][a_x : a_x + (width + 1)]

        for cell in new_cells:
          cell['tile'] = filler

          if meta and (type(meta) == dict):
            cell['meta'] = meta

        self.cell_map[y][a_x : a_x + (width + 1)] = new_cells

    return self.cell_map

  def draw_line(self, a, b, filler, meta=None):
    a_x, a_y = a
    b_x, b_y = b

    slope = (b_y - a_y) / (b_x - a_x)
    x_negative = (b_x - a_x) < 0

    for offset in xrange(abs(b_x - a_x) + 1):
      if x_negative:
        offset = -offset

      x = a_x + offset
      y = int(round(slope * x))

      self.cell_map[y][x]['tile'] = filler

      if meta and (type(meta) == dict):
        self.cell_map[y][x]['meta'] = meta

  def calculate_visible(self, player_position, distance):
    def tile_obstructs_vision(x, y):
      obstacle_types = ['wall']
      cell = self.cell_map[y][x]

      tile = list(filter(lambda x: x.get('id') == cell['tile'], Terrain.tiles))[0]
      return tile['type'] in obstacle_types

    def reveal_tile(x, y):
      self.cell_map[y][x]['meta']['visible'] = True

    # Because reasons
    p_x, p_y = player_position

    for x, y, cell in self.iterate(static=False):
      # First, make sure that we're always resetting visibility
      cell['meta']['visible'] = False

    # Yes, I *am* the dev who will put each arg on it's own line.
    helpers.fieldOfView(
      startX=p_x,
      startY=p_y,
      mapWidth=self.width,
      mapHeight=self.height,
      radius=distance,
      funcVisitTile=reveal_tile,
      funcTileBlocked=tile_obstructs_vision
    )

    return True

  def get_visible(self):
    cell_map = []

    for row in xrange(self.height):
      cell_map.append([{'tile': None, 'meta': {}}] * self.width)

    for x, y, cell in self.iterate(static=False):
      if cell['meta'].get('visible') == True:
        cell_map[y][x] = cell

    return cell_map

  def to_string(self):
    return cPickle.dumps(self.cell_map)

  @classmethod
  def from_string(cls, pickled_grid):
    cell_map = cPickle.loads(pickled_grid)
    height = len(cell_map)
    width = len(cell_map[0])

    return cls(width, height, cell_map)

  # Shorthand methods because reasons
  def rectangle(self, *args):
    return self.fill_rectangle(*args)

  def line(self, *args):
    return self.draw_line(*args)

  def __repr__(self):
    return "".join(["{}\n".format(row) for row in self.cell_map])

  def __str__(self):
    return "<TileGrid size={}x{}>".format(self.width, self.height)
