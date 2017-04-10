from saylua.wrappers import login_required
from saylua.utils import pluralize
from flask import render_template, redirect, flash, request, g
from google.appengine.ext import ndb
from .models.db import Notification


@login_required
def notifications_main():
    per_page = 100
    page = request.args.get('page')
    if not page:
        page = 1
    else:
        page = int(page)
    offset = per_page * (page - 1)

    # TODO: Find a way to use cursors instead of offsets
    notifications, cursor, more = Notification.query(Notification.user_id == g.user.id).order(
        Notification.is_read, -Notification.time).fetch_page(per_page, offset=offset)
    return render_template("notifications/all.html",
        viewed_notifications=notifications, page=page, more_pages=more)


@login_required
def notifications_main_post():
    notification_ids = request.form.getlist('notification_id')
    keys = []
    for n_id in notification_ids:
        n_id = make_ndb_key(n_id)
        if not n_id:
            flash('You are attempting to edit an invalid notification!', 'error')
            return redirect('/notifications/', code=302)
        keys.append(n_id)

    notifications = ndb.get_multi(keys)
    for n in notifications:
        if not n:
            flash('You are attempting to edit a notification which does not exist!', 'error')
            return redirect('/notifications/', code=302)
        if n.user_id != g.user.id:
            flash('You do not have permission to edit these notifications!', 'error')
            return redirect('/notifications/', code=302)
        n.is_read = True

    if 'delete' in request.form:
        ndb.delete_multi(keys)
        flash(pluralize(len(keys), 'notification') + ' deleted. ')
    elif 'read' in request.form:
        ndb.put_multi(notifications)
        flash(pluralize(len(keys), 'notification') + ' marked as read. ')
    return redirect('/notifications/', code=302)


@login_required
def notification_read(key):
    key = make_ndb_key(key)
    if key:
        notification = Notification.get_by_id(key.id())

    if notification and notification.user_id == g.user.id:
        notification.is_read = True
        notification.put()
        return redirect(notification.link, code=302)
    return render_template('notifications/invalid.html')
