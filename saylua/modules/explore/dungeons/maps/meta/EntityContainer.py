from uuid import uuid4
import cPickle

# EntityContainer -> Required by dungeon(s)
# Utility class for the map generators.
# ===================================================


class EntityContainer():
  def __init__(self, entities=None):
    self.entities = entities if entities else []

  def add(self, parent, location, meta=None):
    x, y = location

    new_entity = {
      'id': str(uuid4()),
      'parent': parent,
      'location': {'x': x, 'y': y},
      'meta': meta if meta else {}
    }

    self.entities.append(new_entity)

  def calculate_visible(self, grid):
    # Track unit visibility.
    search = lambda x: x['meta'].get('visible') == True
    visible_tiles = grid.find(search)

    for entity in self.iterate():
      location = (entity['location']['x'], entity['location']['y'])

      if location in visible_tiles:
        entity['meta']['visible'] = True
        entity['meta']['last_location'] = entity['location']
      else:
        # If our entity WAS in vision, and is now not,
        # make sure we track the last seen location.
        if entity['meta'].get('visible') == True:
          entity['meta']['last_location'] = entity['location']

        entity['meta']['visible'] = False

  def get_visible(self):
    entities = []

    for entity in self.iterate():
      if entity['meta'].get('visible') == True:
        entities.append(entity)

    return entities

  def iterate(self):
    for i in range(len(self.entities)):
      yield self.entities[i]

  def get_player(self):
    # Helper method, as this is a common request.
    # This is deliberately not a filter, as the player
    # should always be the first entity.
    return self.entities[0]

  def render(self):
    return self.entities

  def update_entity(self, entity):
    # Replace entity with an updated copy of itself
    for i in xrange(len(self.entities)):
      if self.entities[i]['id'] == entity['id']:
        self.entities[i] = entity
        break

  def to_string(self):
    return cPickle.dumps(self.entities)

  @classmethod
  def from_string(cls, pickled_container):
    return cls(cPickle.loads(pickled_container))
