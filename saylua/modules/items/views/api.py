from saylua import db
from saylua.wrappers import api_login_required
from saylua.utils.pagination import Pagination

from ..models.db import ItemCategory, Item, InventoryItem
from flask import g, request

import json


ITEMS_PER_PAGE = 20


@api_login_required()
def api_inventory(category_id, page):
    inventory_query = db.session.query(InventoryItem).join(Item,
        InventoryItem.item_id == Item.id).filter(
        InventoryItem.user_id == g.user.id)
    if category_id:
        inventory_query = inventory_query.filter(Item.category_id == category_id)
    pagination = Pagination(per_page=ITEMS_PER_PAGE, query=inventory_query,
        current_page=page)

    return json.dumps({'items': [i.to_dict() for i in pagination.items],
        'pages': pagination.page_count, 'categories': [i.to_dict() for i in ItemCategory.all()]})


@api_login_required()
def api_autosale(item_id):
    data = request.get_json()
    entry = db.session.query(InventoryItem).get(item_id, g.user.id)
    amount = data.get('amount')
    if not entry:
        return json.dumps({'error': 'Invalid item.'}), 401
    if amount > entry.count or amount < 0:
        return json.dumps({'error': 'Invalid item quantity entered.'}), 401
    entry.count -= amount

    total_price = amount * entry.item.buyback_price
    g.user.cloud_coins += total_price

    return json.dumps({'message': 'Items sold for %d Cloud Coins.' % total_price})
