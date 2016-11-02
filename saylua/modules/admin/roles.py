from saylua import app, login_required
from flask import (render_template, redirect, make_response,
                   url_for, flash, session, abort, request, g)

from saylua.utils import get_from_request
from saylua.models.role import Role

@app.route('/admin/roles/add/', methods=['GET', 'POST'])
def admin_panel_roles_add():
    if request.method == 'POST':
        name = request.form.get('name')
        new_role = Role(id=name)
        for priv in request.form:
            if priv != 'name':
                setattr(new_role, priv, request.form.get(priv) == 'True')
        new_role.put()
        flash('New Role successfully created!')
        return redirect("/admin/roles/add/")
    privs = Role().to_dict().keys()
    privs.sort()
    return render_template('admin/roles/add.html', privs=privs)

@app.route('/admin/roles/edit/', methods=['GET', 'POST'])
def admin_panel_roles_edit():
    roles = Role.query().fetch()
    privs = Role().to_dict().keys()
    if request.method == 'POST':
        for role in roles:
            for priv in privs:
                setattr(role, priv, ((role.key.id() + "_*_" + priv) in request.form))
            role.put()
        flash("Roles successfully updated!")
    privs.sort()
    return render_template('admin/roles/edit.html', roles=roles, privs=privs)
