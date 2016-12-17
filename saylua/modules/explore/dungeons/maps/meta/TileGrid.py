#from . import Terrain
from . import helpers

import cPickle
import copy


# TileGrid -> Required by dungeon(s)
# Utility class for the map generators.
# ===================================================


class TileGrid():
  def __init__(self, width, height, cell_map=None, default_tile=None):
    self.width = width
    self.height = height

    self.frozen_map = None
    self.locks = 0

    if cell_map:
      self.cell_map = cell_map

    else:
      # Populate with empty cells
      self.cell_map = []

      default_cell = {
        'tile': default_tile,
        'meta': {}
      }

      for row in xrange(height):
        self.cell_map.append([copy.deepcopy(default_cell) for i in range(width)])

  def __lock(self):
    if self.locks == 0:
      self.frozen_map = copy.deepcopy(self.cell_map)

    self.locks += 1

  def __unlock(self):
    self.locks -= 1

    if self.locks == 0:
      del self.frozen_map

  def __get_cell_map(self):
    if self.locks > 0:
      return self.frozen_map
    else:
      return self.cell_map

  def _debug_print(self, default_tile):
    def translate(cell):
      return '0' if cell.get('tile') == default_tile else '1'

    def flatten_row(row):
      return "".join([translate(cell) for cell in row])

    print("Debug {}x{}".format(self.width, self.height))
    print("\n".join([flatten_row(row) for row in self.cell_map]))
    print("\n")

  def get(self, a, b=None):
    # Default to returning a single cell,
    # return an array subset if a second argument is provided.
    a_x, a_y = a

    cell_map = self.__get_cell_map()

    if b is None:
      try:
        return cell_map[a_y][a_x]
      except IndexError:
        return False

    else:
      sub_map = []
      b_x, b_y = b

      height = b_y - a_y
      width = b_x - a_x

      for offset in xrange(height + 1):
        y = a_y + offset

        if 0 <= y < self.height:
          # Ensure our select doesn't go out of bounds.
          x_left = max(a_x, 0)
          x_right = min((a_x + width + 1), (self.width - 1))

          cells = cell_map[y][x_left:x_right]
          sub_map.append(cells)

      return sub_map

  def set(self, coords, value=None, meta=None):
    x, y = coords

    try:
      if value:
        self.cell_map[y][x]['tile'] = value

      if meta and (type(meta) == dict):
        self.cell_map[y][x]['meta'] = meta

    except IndexError:
      print("Tried filling ({}, {}), and failed. You really messed up.".format(x, y))
      raise

  def find(self, search_function):
    # Returns a list of tupled cell locations that satisfy <search_function>
    results = []

    for x, y, cell in self.iterate():
      if search_function(cell):
        results.append((x, y))

    return results

  def iterate(self):
    # Generator that yields cells. Exists for performance / niceness reasons.
    # Works from a copy so that iterators can edit the object's grid in-place.
    # Will ensure all read operations occur on a copy of the map until finished.

    self.__lock()
    working_set = self.__get_cell_map()

    for y in xrange(self.height):
      for x in xrange(self.width):
        yield (x, y, working_set[y][x])

    self.__unlock()

  def fill_circle(self, center, radius, filler, meta=None):
    # Fill circles from the center, with radius of N.
    c_x, c_y = center

    for x, y, cell in self.iterate():
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

      if 0 <= y < self.height:
        # Ensure our selects don't go out of bounds.
        x_left = max(a_x, 0)
        x_right = min((a_x + width + 1), (self.width - 1))

        # Make sure we're not inserting more cells than exist
        selected_cells = self.cell_map[y][x_left:x_right]

        for cell in selected_cells:
          cell['tile'] = filler

          if meta and (type(meta) == dict):
            cell['meta'] = meta

        self.cell_map[y][x_left:x_right] = selected_cells

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

      matching_tile = filter(lambda tile: tile.get('id') == cell['tile'], Terrain.tiles)
      matching_tile = list(matching_tile)[0]

      return matching_tile['type'] in obstacle_types

    def reveal_tile(x, y):
      self.cell_map[y][x]['meta']['visible'] = True

    # Because reasons
    p_x, p_y = player_position

    for x, y, cell in self.iterate():
      # First, make sure that we're always resetting visibility
      self.cell_map[y][x]['meta']['visible'] = False

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

  def get_visible(self):
    cell_map = []

    for row in xrange(self.height):
      cell_map.append([copy.copy({}) for i in range(self.width)])

    for x, y, cell in self.iterate():
      if cell['meta'].get('visible') == True:
        cell_map[y][x] = cell

    return cell_map

  def render(self):
    return self.cell_map

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
