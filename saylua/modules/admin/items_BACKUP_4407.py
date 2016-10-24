from saylua import app, login_required
from flask import (render_template, redirect, make_response,
                   url_for, flash, session, abort, request, g)

<<<<<<< HEAD
@app.route('/admin/items/add/', methods=['GET'])
def admin_panel_items_add():
    return render_template('admin/items/add.html')
=======
from saylua.utils import get_from_request
from saylua.models.item import Item

@app.route('/admin/items/add/', methods=['GET', 'POST'])
def admin_panel_items_add():
    name = get_from_request(request, 'name')
    category = get_from_request(request, 'category')
    description = get_from_request(request, 'description')
    if request.method == 'POST':
        image_url = request.form.get('image_url')
        item = Item(name=name, category=category, image_url=image_url,
            url_name=Item.make_url_name(name), description=description)
        item.put()
        flash('You have successfully created a new item! ')
        return redirect(url_for('admin_panel_items_add'))
    return render_template('admin/items/add.html', name=name, category=category, description=description)
>>>>>>> f63de97b46b141f7bc01e2cfb2e026ef51c2db8d

@app.route('/admin/items/edit/', methods=['GET'])
def admin_panel_items_edit():
    return render_template('admin/items/edit.html')
