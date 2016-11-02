from saylua import app, login_required
from flask import (render_template, redirect, make_response,
                   url_for, flash, session, abort, request, g)

from google.appengine.ext import ndb
from saylua.models.role import Role

@app.route('/admin/setupdb/', methods=['GET'])
def setup_db():
    #Create the role 'admin' with all privileges
    admin_role = Role(id='admin')
    admin_dict = admin_role.to_dict()
    for entry in admin_dict:
        setattr(admin_role, entry, True)
    admin_role.put()

    flash("Database Setup Complete")
    return redirect("/admin/")
