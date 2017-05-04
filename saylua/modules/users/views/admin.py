from saylua.wrappers import admin_access_required
from flask import render_template, request, g

from saylua.models.user import User, InviteCode
from saylua import db


@admin_access_required
def user_manage():
    users = db.session.query(User).all()
    return render_template('admin/manage.html', users=users)


@admin_access_required
def user_invite():
    if request.form.get("generate"):
        new_code = InviteCode(g.user.id)
        db.session.add(new_code)
        db.session.commit()
    codes = db.session.query(InviteCode).order_by(InviteCode.date_created.asc()).limit(30)
    return render_template('admin/invite.html', codes=codes)
