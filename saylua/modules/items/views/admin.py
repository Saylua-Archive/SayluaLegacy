from saylua import app, db

from saylua.utils import get_from_request
from saylua.wrappers import admin_access_required

from ..models.db import Item, ItemCategory
from ..forms import ItemUploadForm

from flask import render_template, redirect, url_for, flash, request

import cloudstorage as gcs


@admin_access_required()
def admin_panel_items_add():
    form = ItemUploadForm(request.form)
    form.name.data = get_from_request(request, 'name')
    form.description.data = get_from_request(request, 'description')

    categories = ItemCategory.get_categories()

    form.category_id.choices = [(i, c) for (i, c) in enumerate(categories)]

    if form.validate_on_submit():
        item = Item()
        form.populate_obj(item)
        db.session.add(item)
        db.session.commit()
        item_image = request.files.get('image')
        if not item_image:
            flash("An item image is required!")
            return render_template('admin/add.html', form=form)
        filename = app.config['IMAGE_BUCKET_NAME'] + "/items/" + item.canon_name + ".png"
        write_retry_params = gcs.RetryParams(backoff_factor=1.1)
        gcs_file = gcs.open(filename,
                          'w',
                          content_type='image/png',
                          options={'x-goog-acl': 'public-read'},
                          retry_params=write_retry_params)
        gcs_file.write(item_image.read())
        gcs_file.close()
        flash('You have successfully created a new item!')
        return redirect(url_for('items.admin_add'))
    return render_template('admin/add.html', form=form)


@admin_access_required()
def admin_panel_items_edit():
    return render_template('admin/edit.html')
