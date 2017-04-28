from saylua.wrappers import admin_access_required
from flask import render_template

from saylua.models.user import User
from saylua import db


@admin_access_required
def user_manage():
    users = db.session.query(User).all()
    return render_template('admin/manage.html', users=users)
