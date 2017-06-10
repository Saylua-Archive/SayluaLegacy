from saylua import db
from saylua.wrappers import login_required
from saylua.utils.pagination import Pagination

from ..models.db import Item, InventoryItem
from flask import render_template, g


@login_required()
def items_inventory(category=None):
    inventory_query = db.session.query(InventoryItem).filter(InventoryItem.user_id == g.user.id)
    pagination = Pagination(per_page=20, query=inventory_query)
    return render_template('inventory.html', pagination=pagination, category=category)


def items_view_all():
    items_query = db.session.query(Item)
    pagination = Pagination(per_page=20, query=items_query)
    return render_template('database/all.html', pagination=pagination)


def items_view_single(canon_name):
    item = Item.by_canon_name(canon_name)
    if not item:
        return render_template('database/invalid.html')
    return render_template('database/view.html', item=item)
