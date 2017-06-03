from saylua.wrappers import admin_access_required
from flask import render_template, request, g, redirect, url_for, flash

from saylua.modules.users.models.db import User, InviteCode, BanLog, BanTypes, Title, RUserTitles
from saylua import db

from saylua.utils.pagination import Pagination

from ..forms.admin import BanForm, MuteForm
from ..forms.settings import DetailsForm

import datetime


@admin_access_required()
def user_manage():
    username = request.args.get('username')
    if username:
        return redirect(url_for('users.admin_manage_single', username=username))
    users_query = db.session.query(User)

    pagination = Pagination(per_page=30, query=users_query)
    return render_template('admin/manage.html', pagination=pagination)


@admin_access_required()
def user_manage_single(username):
    user = User.by_username(username)
    if not user:
        flash(username + ' is not a valid username.')
        return redirect(url_for('users.admin_manage'))

    form = DetailsForm(request.form, obj=user)
    if request.form.get('details') and form.validate_on_submit():
        form.populate_obj(user)
        db.session.commit()
        flash("You have changed the %s's details." % user.name)
    elif request.form.get('edit_title'):
        title_action = request.form.get('edit_title')
        try:
            title_id = int(request.form.get('title_id'))
        except ValueError:
            flash('Invalid title entered.', 'error')

        title = db.session.query(Title).get(title_id)
        if not title:
            flash('Title not found.', 'error')
        elif title_action == 'remove':
            # Remove the user's current title if it's being deleted from their account.
            if user.title_id == title_id:
                user.title_id = None
            db.session.query(RUserTitles).filter(RUserTitles.user_id == user.id,
                RUserTitles.title_id == title_id).delete()
            db.session.commit()
            flash("You've successfully removed %s from %s's titles." % (title.name, user.name))
        elif title_action == 'add':
            user_title = RUserTitles(user_id=user.id, title_id=title_id)
            db.session.merge(user_title)
            db.session.commit()
            flash("You've added %s to %s's titles." % (title.name, user.name))

    titles = db.session.query(Title).all()

    return render_template('admin/manage_single.html', form=form, user=user,
        titles=titles)


@admin_access_required()
def user_ban(username):
    user = User.by_username(username)
    if not user:
        flash(username + ' is not a valid username.')
        return redirect(url_for('users.admin_manage'))

    ban_form = BanForm(request.form)
    mute_form = MuteForm(request.form)

    form = None
    if request.form.get('ban'):
        ban_type = BanTypes.BAN
        form = ban_form
    elif request.form.get('mute'):
        ban_type = BanTypes.MUTE
        form = mute_form
    elif user.ban and request.form.get('undo'):
        ban = user.ban
        user.ban.date_unbanned = datetime.datetime.now()
        user.ban_id = None
        db.session.commit()
        flash('You have successfully %s %s.' % (ban.past_tense(), user.name))
    elif request.method == 'POST':
        flash('Invalid ban type!', 'error')
        return render_template('admin/ban.html', ban_form=ban_form, mute_form=mute_form, user=user)

    if form and form.validate_on_submit():
        ban = BanLog(user=user, ban_type=ban_type)

        if form.days.data and form.is_permanent.data:
            flash("You can't both permanently and temporarily %s a user." % ban.verb(), 'error')
            return render_template('admin/ban.html', ban_form=ban_form, mute_form=mute_form, user=user)
        if form.days.data:
            ban.banned_until = datetime.datetime.now() + datetime.timedelta(days=form.days.data)
            timeframe = "for %d days" % form.days.data
        else:
            timeframe = "permanently"
        form.populate_obj(ban)
        db.session.add(ban)
        db.session.commit()

        user.ban = ban
        db.session.commit()

        flash("User %s has been %s %s." % (user.name, ban.past_tense(), timeframe))
    return render_template('admin/ban.html', ban_form=ban_form, mute_form=mute_form, user=user)


@admin_access_required()
def user_invite():
    if request.form.get("generate"):
        new_code = InviteCode(g.user.id)
        db.session.add(new_code)
        db.session.commit()
    codes = db.session.query(InviteCode).order_by(InviteCode.date_created.asc()).limit(30).all()
    return render_template('admin/invite.html', codes=codes)
