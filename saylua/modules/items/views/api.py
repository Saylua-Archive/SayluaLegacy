from saylua import db
from saylua.wrappers import api_login_required
from saylua.utils.pagination import Pagination

from ..models.db import Item, InventoryItem
from flask import g

import json


ITEMS_PER_PAGE = 20


@api_login_required()
def api_inventory(category_id, page):
    inventory_query = db.session.query(InventoryItem).join(Item,
        InventoryItem.item_id == Item.id).filter(
        InventoryItem.user_id == g.user.id, Item.category_id == category_id)
    pagination = Pagination(per_page=ITEMS_PER_PAGE, query=inventory_query,
        current_page=page)

    return json.dumps({'items': [i.to_dict() for i in pagination.items],
        'pages': pagination.page_count})
