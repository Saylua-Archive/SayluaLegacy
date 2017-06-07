from saylua import app, db

from saylua.utils import get_from_request
from saylua.wrappers import admin_access_required

from .models.db import Item

from flask import render_template, redirect, url_for, flash, request
from forms import ItemUploadForm
import cloudstorage as gcs


@admin_access_required()
def admin_panel_items_add():
    form = ItemUploadForm(request.form)
    form.name.data = get_from_request(request, 'name')
    form.description.data = get_from_request(request, 'description')
    if form.validate_on_submit():
        item = Item()
        form.populate_obj(item)
        db.session.add(item)
        db.session.commit()
        item_image = request.form.get('image')
        filename = app.config['IMAGE_BUCKET_NAME'] + "/items/" + item.canon_name + ".png"
        write_retry_params = gcs.RetryParams(backoff_factor=1.1)
        gcs_file = gcs.open(filename,
                          'w',
                          content_type='image/png',
                          options={},
                          retry_params=write_retry_params)
        gcs_file.write(item_image.encode('utf-8'))
        gcs_file.close()
        flash('You have successfully created a new item!')
        return redirect(url_for('items.admin_add'))
    return render_template('admin/add.html', form=form)


@admin_access_required()
def admin_panel_items_edit():
    return render_template('admin/edit.html')
