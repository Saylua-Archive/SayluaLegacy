from saylua import app

from saylua.utils import get_static_version_id

from flask import url_for

from functools import partial

import os
import random


# Injected functions.

@app.context_processor
def inject_include_static():
    def include_static(file_path):
        return '/static' + '/' + file_path + '?v=' + str(get_static_version_id())

    return dict(include_static=include_static)


@app.context_processor
def inject_random_pet_image():
    species = ['eydrun', 'loxi', 'arko', 'chirling', 'gorbin', 'senrix', 'nylik',
        'gam', 'vela', 'fleuran']

    def random_pet_image():
        return '/static/img/pets/' + random.choice(species) + '/common.png'

    return dict(random_pet_image=random_pet_image)
