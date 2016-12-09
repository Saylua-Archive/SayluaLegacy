from saylua import app
from .models.db import Item
from flask import render_template

import os, random


def items_inventory(category=None):
    path = os.path.join(app.static_folder, 'img/items/160/')
    items = []

    for i in xrange(60):
        name = random.choice(os.listdir(path))
        items.append({'name': name, 'img_url': '/static/img/items/160/' + name})

    return render_template('inventory.html', items=items, category=category)


@app.route('/items/', methods=['GET'])
def items_view_all():
    items = Item.query().fetch(20)
    return render_template('database/all.html', items=items)


@app.route('/item/<url_name>/', methods=['GET'])
def items_view_single(url_name):
    item = Item.by_url_name(url_name)
    if not item:
        return render_template('items/database/invalid.html')
    return render_template('database/view.html', item=item)
