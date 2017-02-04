from saylua.modules.explore.models.db import DungeonEntity, DungeonTile
from . import map_list
import random


class Dungeon:
    def __init__(self, type="random", options=None):
        # Determine our Dungeon type
        if type == "random":
            map_types = list(map_list.keys())
            self.type = random.choice(map_types)
            self.api = map_list[self.type]

        else:
            self.type = type
            self.api = map_list[self.type]

        # Store tile_set, entity_set
        tile_set = self.api.get("tile_set")
        entity_set = self.api.get("entity_set")

        # Resolve to the real tile_set, entity_set from names
        raw_tile_set = DungeonTile.query.filter(DungeonTile.name.in_(tile_set)).all()
        raw_entity_set = DungeonEntity.query.filter(DungeonEntity.name.in_(entity_set)).all()

        # Reduce to JSON objects and store on the class
        self.tile_set = [tile.to_dict() for tile in raw_tile_set]
        self.entity_set = [entity.to_dict() for entity in raw_entity_set]

        # Generate Dungeon
        self.options = options or self.api.get("default_options")
        self.grid = self.api.generate(self.options)

        # Iterate Dungeon
        for i in xrange(self.options.get('iterations', 1)):
            self.api.iterate(self.options, self.grid)

        # Make last-step changes.
        self.api.finalize(self.options, self.grid)

        # Create our entity layer.
        self.entities = self.api.populate(self.options, self.grid)

    def get_info(self):
        return {
            "type": self.type,
            "options": self.options
        }
