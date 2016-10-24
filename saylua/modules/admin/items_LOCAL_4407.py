from saylua import app, login_required
from flask import (render_template, redirect, make_response,
                   url_for, flash, session, abort, request, g)

@app.route('/admin/items/add/', methods=['GET'])
def admin_panel_items_add():
    return render_template('admin/items/add.html')

@app.route('/admin/items/edit/', methods=['GET'])
def admin_panel_items_edit():
    return render_template('admin/items/edit.html')
