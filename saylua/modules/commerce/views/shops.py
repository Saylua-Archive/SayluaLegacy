from saylua import db
from flask import render_template, request, g, flash

from saylua.modules.items.models.db import Item
from saylua.modules.users.models.db import InvalidCurrencyException
from saylua.utils import int_or_none

from saylua.wrappers import login_required


@login_required()
def npc_shop_view(name):
    items = db.session.query(Item).all()

    purchase_id = int_or_none(request.form.get('item_id'))
    amount = int_or_none(request.form.get('amount'))
    if purchase_id and purchase_id > 0 and amount and amount > 0:
        purchase = db.session.query(Item).get(purchase_id)
        entry = purchase.give_items(g.user.id, amount)

        try:
            price = purchase.buyback_price
            g.user.cloud_coins -= price * amount
            db.session.add(entry)
            db.session.commit()
            flash("You've successfully purchased %d %s for %d cloud coins." % (amount, purchase.name, amount * price))
        except InvalidCurrencyException:
            flash('You do not have the funds to purchase this item.', 'error')
    return render_template("shops/npc.html", items=items)
