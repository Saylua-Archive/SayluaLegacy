from saylua.wrappers import login_required
from saylua.utils import pluralize
from flask import render_template, redirect, flash, request, g
from saylua import db
from .models.db import Notification
import flask_sqlalchemy


@login_required
def notifications_main():
    NOTIFICATIONS_PER_PAGE = 100
    page_number = request.args.get('page')
    if not page_number:
        page_number = 1
    else:
        page_number = int(page_number)
    offset = NOTIFICATIONS_PER_PAGE * (page_number - 1)

    notifications = (
        db.session.query(Notification)
        .filter(Notification.user_id == g.user.id)
        .filter(Notification.unread == True)
        .order_by(Notification.time.desc())
        .limit(NOTIFICATIONS_PER_PAGE)
        .offset(offset)
        .all()
    )
    notification_count = (
        db.session.query(Notification.user_id)
        .filter(Notification.user_id == g.user.id)
        .filter(Notification.unread == True)
        .count()
    )
    more = notification_count > page_number * NOTIFICATIONS_PER_PAGE
    return render_template("notifications/all.html",
        viewed_notifications=notifications, page=page_number, more_pages=more)


@login_required
def notifications_main_post():
    notification_ids = request.form.getlist('notification_id')
    keys = []
    for n_id in notification_ids:
        if not n_id:
            flash('You are attempting to edit an invalid notification!', 'error')
            return redirect('/notifications/', code=302)
        keys.append(n_id)

    for key in keys:
        try:
            found_notification = db.session.query(Notification).get(key)
            if found_notification.user_id != g.user.id:
                flash('You do not have permission to edit these notifications!', 'error')
                return redirect('/notifications/', code=302)
            if 'delete' in request.form:
                db.session.delete(found_notification)
            elif 'read' in request.form:
                found_notification.unread = False
                db.session.add(found_notification)
        except(flask_sqlalchemy.orm.exc.NoResultFound):
            flash('You are attempting to edit a notification which does not exist!', 'error')
            return redirect('/notifications/', code=302)
        if 'delete' in request.form:
            flash(pluralize(len(keys), 'notification') + ' deleted. ')
        elif 'read' in request.form:
            flash(pluralize(len(keys), 'notification') + ' marked as read. ')
    db.session.commit()
    return redirect('/notifications/', code=302)


@login_required
def notification_read(key):
    try:
        found_notification = db.session.query(Notification).get(key)
        if found_notification and found_notification.user_id == g.user.id:
            found_notification.unread = False
            db.session.commit()
            return redirect(found_notification.link, code=302)
        else:
            return render_template('notifications/invalid.html')
    except(flask_sqlalchemy.orm.exc.NoResultFound):
        return render_template('notifications/invalid.html')
