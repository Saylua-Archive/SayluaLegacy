from saylua import app
from flask import (render_template, redirect,
                   url_for, flash, session, abort, request)
import os, random

@app.route('/inventory/')
def items_inventory():
    path = os.path.join(app.static_folder, 'img/items/160/')
    items = []

    for i in xrange(60):
        name = random.choice(os.listdir(path))
        items.append({'name': name, 'img_url': '/static/img/items/160/' + name})

    return render_template('items/inventory.html', items=items)
