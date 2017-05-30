from flask import render_template, redirect, g, flash, request

from saylua import db, app

from saylua.wrappers import moderation_access_required, communication_access_required, login_required
from saylua.utils.pagination import Pagination

from .models.db import Board, BoardCategory, ForumThread, ForumPost, ForumSubscription
from .forms.main import ForumThreadForm, ForumPostForm


def forums_home():
    categories = BoardCategory.get_categories()
    return render_template("forums_home.html", categories=categories)


# Viewing a forum board and adding new threads to it.
def forums_board(canon_name):
    board = Board.by_canon_name(canon_name)

    if not board:
        return render_template('404.html'), 404

    form = ForumThreadForm(request.form)

    if request.method == 'POST' and not board.can_post(g.user):
        flash("You do not have permission to post a new thread.", 'error')
    elif form.validate_on_submit():
        title = request.form.get('title')
        body = request.form.get('body')
        author = g.user
        board_id = board.id
        new_thread = ForumThread(title=title, author_id=author.id, board_id=board_id)
        new_post = ForumPost(author_id=author.id, thread=new_thread, body=body)

        author.post_count += 1

        # If the user wants to autosubscribe to threads they create.
        if author.autosubscribe_threads:
            subscription = ForumSubscription(user=author, thread=new_thread)
            db.session.add(subscription)

        db.session.add(new_thread)
        db.session.add(new_post)
        db.session.commit()

        flash("You've posted a new thread.")
        return redirect(new_thread.url())

    threads_query = (
        db.session.query(ForumThread)
        .filter(ForumThread.board_id == board.id)
        .order_by(ForumThread.is_pinned.desc(), ForumThread.date_modified.desc())
    )

    pagination = Pagination(per_page=app.config.get('THREADS_PER_PAGE'), query=threads_query)

    return render_template("board.html", form=form, board=board, pagination=pagination)


# Viewing a forum thread and adding new posts to it.
def forums_thread(thread, page=1):
    try:
        thread_id = int(thread.split('-', 1)[0])
    except:
        return render_template('404.html'), 404

    form = ForumPostForm(request.form)

    thread = db.session.query(ForumThread).filter(ForumThread.id == thread_id).one_or_none()

    if not thread:
        return render_template('404.html'), 404

    if request.method == 'POST' and not thread.can_post(g.user):
        flash("You do not have permission to reply to forum threads.", 'error')
    elif form.validate_on_submit():
        author = g.user
        body = request.form.get('body')
        new_post = ForumPost(author_id=author.id, thread_id=thread_id, body=body)
        author.post_count += 1

        # If the user wants to autosubscribe to threads they post on.
        if author.autosubscribe_posts and not thread.subscription(author):
            subscription = ForumSubscription(user=author, thread=thread)
            db.session.add(subscription)

        db.session.add(new_post)
        db.session.commit()

        # Notify all subscribed users about the new post. Note, this should be
        # optimized later.
        thread.notify_subscribers(new_post)

        flash("You've successfully made a new forum post.")
        return redirect(new_post.url())

    post_query = (
        db.session.query(ForumPost)
        .filter(ForumPost.thread_id == thread_id)
        .order_by(ForumPost.date_created)
    )

    pagination = Pagination(per_page=app.config.get('POSTS_PER_PAGE'), query=post_query,
        current_page=page, url_base=thread.url(), url_end='/')

    other_boards = db.session.query(Board).all()

    return render_template("thread.html", form=form, thread=thread,
            pagination=pagination, other_boards=other_boards)


@moderation_access_required
def forums_thread_move(thread_id):
    thread = db.session.query(ForumThread).filter(ForumThread.id == thread_id).one_or_none()

    if not thread:
        return render_template('404.html'), 404

    if 'move' in request.form:
        destination = int(request.form.get('destination'))
        thread.board_id = destination
        db.session.commit()
        flash("Thread moved successfully!")
    return redirect(thread.url())


@moderation_access_required
def forums_thread_pin(thread_id):
    thread = db.session.query(ForumThread).filter(ForumThread.id == thread_id).one_or_none()
    if not thread:
        return render_template('404.html'), 404

    if 'pin' in request.form:
        thread.is_pinned = True
        db.session.commit()
        flash("You've successfully pinned this thread.")
    elif 'unpin' in request.form:
        thread.is_pinned = False
        db.session.commit()
        flash("You've successfully unpinned this thread.")
    else:
        flash("Invalid pin state.", 'error')

    return redirect(thread.url())


@moderation_access_required
def forums_thread_lock(thread_id):
    thread = db.session.query(ForumThread).filter(ForumThread.id == thread_id).one_or_none()
    if not thread:
        return render_template('404.html'), 404

    if 'lock' in request.form:
        thread.is_locked = True
        db.session.commit()
        flash("You've successfully locked this thread.")
    elif 'unlock' in request.form:
        thread.is_locked = False
        db.session.commit()
        flash("You've successfully unlocked this thread.")
    else:
        flash("Invalid pin state.", 'error')

    return redirect(thread.url())


@login_required
def forums_thread_subscribe(thread_id):
    thread = db.session.query(ForumThread).filter(ForumThread.id == thread_id).one_or_none()
    if not thread:
        return render_template('404.html'), 404

    subscription = thread.subscription(g.user)
    if 'subscribe' in request.form:
        if subscription:
            flash("You are already subscribed to this thread.")
        else:
            subscription = ForumSubscription(user=g.user, thread=thread)
            db.session.add(subscription)
            db.session.commit()
            flash("You've successfully subscribed to this thread.")
    elif 'unsubscribe' in request.form:
        if not subscription:
            flash("You're not subscribed to this thread.")
        else:
            db.session.delete(subscription)
            db.session.commit()
            flash("You've successfully unsubscribed from this thread.")
    else:
        flash("Invalid subscription state.", 'error')
    return redirect(thread.url())


@communication_access_required
def forums_post_edit(post_id):
    post = db.session.query(ForumPost).get(post_id)
    if not post:
        return render_template('404.html'), 404

    if not post.can_edit(g.user):
        flash('You do not have permission to edit this post.', 'error')
        return redirect(post.url())

    form = ForumPostForm(request.form, obj=post)
    if form.validate_on_submit():
        form.populate_obj(post)
        db.session.add(post)
        db.session.commit()
        flash("You've edited your post. ")
        return redirect(post.url())

    return render_template('post_edit.html', post=post, form=form)
