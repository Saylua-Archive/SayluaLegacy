from saylua import app, login_required
from flask import (render_template, redirect, make_response,
                   url_for, flash, session, abort, request, g)

from saylua.utils import get_from_request
from saylua.utils.form import flash_errors

from saylua.models.item import Item

from forms import ItemUploadForm

@app.route('/admin/items/add/', methods=['GET', 'POST'])
def admin_panel_items_add():
    form = ItemUploadForm(request.form)
    form.name.data = get_from_request(request, 'name')
    form.description.data = get_from_request(request, 'description')
    if request.method == 'POST' and form.validate():
        item = Item.create(name=form.name.data, image_url=form.image_url.data,
            description=form.description.data)
        item.put()
        flash('You have successfully created a new item! ')
        return redirect(url_for('admin_panel_items_add'))
    flash_errors(form)
    return render_template('admin/items/add.html', form=form)

@app.route('/admin/items/edit/', methods=['GET'])
def admin_panel_items_edit():
    return render_template('admin/items/edit.html')
