from saylua import app
from flask import (render_template, redirect,
                   url_for, flash, session, abort, request)

import json, random

@app.route('/api/explore/map/')
def api_map_generation():
    # TODO: Make sure to authorize player for viewing map
    explore_map = ExploreMap(10, 10)
    return explore_map.json()

@app.route('/api/explore/move/', methods=['POST'])
def api_map_move():
    if not (request.form and request.form["x"] and request.form["y"]):
        return json.dumps({'Error' : 'Bad API Usage. '}), 400

    result = {}

    return json.dumps(result)


class MapActor:
    def __init__(self, actor_type, x, y):
        self.type = actor_type
        self.x = x
        self.y = y

    def move(self, map):
        if actor_type == 'pet':
            self.move_randomly()

    def move_randomly(self, map):
        directions = random.shuffle([{'x': 1}, {'x': -1}, {'y': 1}, {'y': -1}])
        for movement in directions:
            new_x = self.x
            new_y = self.y
            if movement.x:
                new_x += movement.x
            if movement.y:
                new_y += movement.y
            if map.is_valid_square(new_x, new_y):
                self.x = new_x
                self.y = new_y
                return True
        return False

class MapTile:
    walkable_tiles = {'dirt'}
    def __init__(self, tile_type):
        self.change_type(tile_type)
        self.event_triggered = False
        self.landmark = ''

    def change_type(self, tile_type):
        self.type = tile_type
        self.walkable = tile_type in MapTile.walkable_tiles

    def set_landmark(self, landmark):
        self.landmark = landmark

    def trigger_event():
        if self.event_triggered:
            return False
        self.event_triggered = True
        return True

    def walkable(self):
        return self.walkable

    def json(self):
        return json.dumps(self.__dict__)

# Class to represent the map that the player is currently exploring on
class ExploreMap:
    def __init__(self, x_count, y_count):
        self.x_count = x_count
        self.y_count = y_count
        self.actors = []
        self.map = [0] * x_count * y_count

        self.generate_map()
        while self.count_valid_squares() < x_count * y_count / 2:
            self.generate_map()

        # Get Player location
        self.player_location = self.get_walkable_square()

        # Generate exit location
        exit = self.get_walkable_square()
        while exit == self.player_location:
            exit = self.get_walkable_square()

        # Generate actors
        while random.randint(0, 1) > 0:
            actor_location =  self.get_walkable_square()
            while actor_location == self.player_location:
                actor_location = self.get_walkable_square()
            self.actors.append(MapActor('pet', actor_location['x'], actor_location['y']))

        # Convert map to Tile objects
        self.generate_object_map()

        self.get_square(exit['x'], exit['y']).set_landmark('exit')

    def generate_object_map(self):
        new_map = [None] * len(self.map)
        for i in xrange(0, len(self.map)):
            if self.map[i] > 0:
                new_map[i] = MapTile('dirt')
            else:
                if random.randint(0, 5) > 4:
                    new_map[i] = MapTile('water')
                else:
                    new_map[i] = MapTile('cave_wall')
        self.map = new_map

    def is_valid_square(self, x, y):
        return x >= 0 and x < self.x_count and y >= 0 and y < self.y_count

    def get_square(self, x, y):
        return self.map[y * self.x_count + x]

    def set_square(self, x, y, val):
        self.map[y * self.x_count + x] = val

    def generate_map(self):
        self.fill_map_randomly()
        curr = self.get_walkable_square()
        new_map = [0] * self.x_count * self.y_count
        self.flood_find(curr['x'], curr['y'], new_map)
        self.map = new_map

    def count_valid_squares(self):
        result = 0
        for i in xrange(0, len(self.map)):
            if self.map[i] > 0:
                result += 1
        return result

    def get_walkable_square(self):
        curr_x = random.randint(0, self.x_count - 1)
        curr_y = random.randint(0, self.y_count - 1)
        while self.get_square(curr_x, curr_y) == 0:
            curr_x = random.randint(0, self.x_count - 1)
            curr_y = random.randint(0, self.y_count - 1)
        return {'x': curr_x, 'y': curr_y}

    def fill_map_randomly(self):
        for i in xrange(self.x_count * self.y_count):
            self.map[i] = random.randint(0, 1)

    def flood_find(self, x, y, new_map):
        if (not self.is_valid_square(x, y) or self.get_square(x, y) == 0):
            return
        self.set_square(x, y, 0)
        new_map[y * self.x_count + x] = 1

        self.flood_find(x + 1, y, new_map)
        self.flood_find(x - 1, y, new_map)
        self.flood_find(x, y + 1, new_map)
        self.flood_find(x, y - 1, new_map)

    def json_map(self):
        result = [None] * len(self.map)
        for i in xrange(0, len(self.map)):
            result[i] = self.map[i].__dict__
        return result

    def json_actors(self):
        result = [None] * len(self.actors)
        for i in xrange(0, len(self.actors)):
            result[i] = self.actors[i].__dict__
        return result

    def json(self):
        return json.dumps({'player': self.player_location, 'actors': self.json_actors(), 'map': self.json_map()})
