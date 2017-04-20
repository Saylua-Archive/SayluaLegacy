from saylua import db

from .models.db import Item
from flask import render_template


def items_inventory(category=None):
    return render_template('inventory.html', category=category)


def items_view_all():
    items = db.session.query(Item)
    return render_template('database/all.html', items=items)


def items_view_single(url_name):
    item = Item.by_url_name(url_name)
    if not item:
        return render_template('database/invalid.html')
    return render_template('database/view.html', item=item)
