from flask import render_template, g, redirect, flash
from saylua.wrappers import login_required
from saylua import db
from saylua.utils import pluralize
from saylua.modules.items.models.db import Item
from operator import attrgetter
import random


def town_main():
    return render_template("town.html")


@login_required(redirect='views.free_items', error='You need to be logged to get free items!')
def free_items():
    candidates = Item.query.order_by(db.func.random()).limit(3).all()
    choice = min(candidates, key=attrgetter('buyback_price'))
    amount = random.randint(1, 5)
    db.session.add(choice.give_items(g.user.id, amount))
    db.session.commit()
    flash("Rufus gives you " + pluralize(amount, choice.name) + ", for \"free.\"")
    return redirect('/town/', code=302)
