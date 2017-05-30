from saylua.wrappers import admin_access_required
from flask import render_template, request, g, redirect, url_for, flash

from saylua.modules.users.models.db import User, InviteCode
from saylua import db

from saylua.utils.pagination import Pagination

from ..forms.admin import BanForm, MuteForm
from ..forms.settings import DetailsForm


@admin_access_required
def user_manage():
    username = request.args.get('username')
    if username:
        return redirect(url_for('users.admin_manage_single', username=username))
    users_query = db.session.query(User)

    pagination = Pagination(per_page=30, query=users_query)
    return render_template('admin/manage.html', pagination=pagination)


@admin_access_required
def user_manage_single(username):
    user = User.by_username(username)
    if not user:
        flash(username + ' is not a valid username.')
        return redirect(url_for('users.admin_manage'))

    form = DetailsForm(request.form, obj=user)
    if form.validate_on_submit():
        form.populate_obj(user)
        db.session.commit()
        flash("You have changed the %s's details." % user.name)

    return render_template('admin/manage_single.html', form=form, user=user)


@admin_access_required
def user_ban(username):
    user = User.by_username(username)
    if not user:
        flash(username + ' is not a valid username.')
        return redirect(url_for('users.admin_manage'))

    ban_form = BanForm(request.form)
    if request.form.get('ban') and ban_form.validate_on_submit():
        flash("User %s has been banned" % user.name)

    return render_template('admin/ban.html', ban_form=ban_form, user=user)


@admin_access_required
def user_invite():
    if request.form.get("generate"):
        new_code = InviteCode(g.user.id)
        db.session.add(new_code)
        db.session.commit()
    codes = db.session.query(InviteCode).order_by(InviteCode.date_created.asc()).limit(30).all()
    return render_template('admin/invite.html', codes=codes)
