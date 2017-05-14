from saylua import db
from saylua.wrappers import login_required

from .models.db import Item, InventoryItem
from flask import render_template, g


@login_required
def items_inventory(category=None):
    items = db.session.query(InventoryItem).filter(InventoryItem.user_id == g.user.id)
    return render_template('inventory.html', items=items, category=category)


def items_view_all():
    items = db.session.query(Item)
    return render_template('database/all.html', items=items)


def items_view_single(url_name):
    item = Item.by_url_name(url_name)
    if not item:
        return render_template('database/invalid.html')
    return render_template('database/view.html', item=item)
