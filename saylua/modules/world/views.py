from flask import render_template, g, redirect, flash
from saylua.wrappers import login_required
from saylua import db
from saylua.modules.items.models.db import Item
from operator import attrgetter


def town_main():
    return render_template("town.html")


@login_required(redirect='views.free_items', error='You need to be logged to get free items!')
def free_items():
    candidates = Item.query.order_by(db.func.random()).limit(3).all()
    recipient = g.user
    for candidate in candidates:
        flash(candidate.name + " " + str(candidate.buyback_price))
    item = min(candidates, key=attrgetter('buyback_price'))
    flash(item.name)
    return redirect('/home/', code=302)
