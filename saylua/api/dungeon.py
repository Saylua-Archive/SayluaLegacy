from saylua import app
from flask import (render_template, redirect,
                   url_for, flash, session, abort, request)

import json, random

@app.route('/api/explore/map/')
def api_map_generation():
    explore_map = ExploreMap(10, 8)
    return explore_map.json()

class ExploreMap:
    def __init__(self, x_count, y_count):
        self.x_count = x_count
        self.y_count = y_count
        self.map = [0] * x_count * y_count

        self.generate_map()
        while self.count_valid_squres() < x_count * y_count / 2:
            self.generate_map()
        self.player_location = self.get_valid_square()

    def is_valid_square(self, x, y):
        return x >= 0 and x < self.x_count and y >= 0 and y < self.y_count

    def get_square(self, x, y):
        return self.map[y * self.x_count + x]

    def set_square(self, x, y, val):
        self.map[y * self.x_count + x] = val

    def generate_map(self):
        self.fill_map_randomly()
        curr = self.get_valid_square()
        new_map = [0] * self.x_count * self.y_count
        self.flood_find(curr['x'], curr['y'], new_map)
        self.map = new_map

    def count_valid_squres(self):
        result = 0
        for i in xrange(0, len(self.map)):
            if self.map[i] > 0:
                result += 1
        return result

    def get_valid_square(self):
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

    def json(self):
        return json.dumps({'player': self.player_location, 'map': self.map})
