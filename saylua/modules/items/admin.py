from saylua import db

from saylua.utils import get_from_request
from saylua.wrappers import admin_access_required

from .models.db import Item

from flask import render_template, redirect, url_for, flash, request
from forms import ItemUploadForm


@admin_access_required
def admin_panel_items_add():
    form = ItemUploadForm(request.form)
    form.name.data = get_from_request(request, 'name')
    form.description.data = get_from_request(request, 'description')
    if request.method == 'POST' and form.validate():
        item = Item(name=form.name.data, text_id=Item.make_text_id(form.name.data),
            description=form.description.data)
        db.session.add(item)
        db.session.commit()
        flash('You have successfully created a new item!')
        return redirect(url_for('items.items_admin_add'))
    return render_template('admin/add.html', form=form)


@admin_access_required
def admin_panel_items_edit():
    return render_template('admin/edit.html')
