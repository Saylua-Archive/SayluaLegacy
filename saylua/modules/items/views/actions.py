from saylua import db
from saylua.wrappers import login_required

from saylua.utils import int_or_none
from ..models.db import InventoryItem

from flask import g, request, flash, redirect


@login_required()
def bond_mini():
    from saylua.modules.pets.models.db import Pet, MiniFriendship

    data = request.form

    mini_id = int_or_none(data.get('mini_id'))
    pet_id = int_or_none(data.get('pet_id'))

    entry = db.session.query(InventoryItem).get((g.user.id, mini_id))

    if not entry:
        flash("Sorry, the mini you tried to bond is invalid.", 'error')
    elif not pet_id:
        flash("The pet you are trying to edit is invalid.", 'error')
    else:
        pet = db.session.query(Pet).get(pet_id)
        if not pet:
            flash('Pet does not exist.', 'error')
        elif not pet.guardian_id == g.user.id:
            flash('You do not have permission to edit this pet.', 'error')
        else:
            mini = entry.item
            old_mini = pet.mini
            if old_mini:
                old_mini_entry = InventoryItem.give_items(g.user.id, old_mini.id, 1)
                db.session.add(old_mini_entry)
            pet.mini = mini
            entry.count -= 1

            friendship = db.session.query(MiniFriendship).get((pet.id, mini.id))
            if not friendship:
                friendship = MiniFriendship(pet_id=pet.id, mini_id=mini.id)
                db.session.add(friendship)
            db.session.commit()
            flash("%s bonded with %s! May their friendship stay strong!" % (pet.name, mini.name))

    return redirect('/inventory/')


@login_required()
def autosale():
    data = request.form
    amount = int_or_none(data.get('amount'))
    item_id = int_or_none(data.get('item_id'))
    entry = db.session.query(InventoryItem).get((g.user.id, item_id))

    if not entry:
        flash('Invalid item.', 'error')
    elif not amount or amount > entry.count or amount < 0:
        flash('Invalid item quantity entered.', 'error')
    else:
        entry.count -= amount

        total_price = amount * entry.item.buyback_price
        g.user.cloud_coins += total_price
        db.session.commit()
        flash('%d items sold for %d Cloud Coins.' % (amount, total_price))

    return redirect('/inventory/')
