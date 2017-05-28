from flask import render_template, redirect, g, flash, request

from saylua import db

from saylua.wrappers import moderation_access_required
from saylua.utils.pagination import Pagination

from .models.db import Board, BoardCategory, ForumThread, ForumPost
from .forms.main import ForumThreadForm, ForumPostForm


THREADS_PER_PAGE = 10
POSTS_PER_PAGE = 10


def forums_home():
    categories = BoardCategory.get_categories()
    return render_template("forums_home.html", categories=categories)


def forums_board(canon_name):
    board = Board.by_canon_name(canon_name)

    if not board:
        return render_template('404.html'), 404

    form = ForumThreadForm(request.form)

    if form.validate_on_submit():
        title = request.form.get('title')
        body = request.form.get('body')
        author_id = g.user.id
        board_id = board.id
        new_thread = ForumThread(title=title, author_id=author_id, board_id=board_id)
        new_post = ForumPost(author_id=author_id, thread=new_thread, body=body)
        db.session.add(new_thread)
        db.session.add(new_post)
        db.session.commit()
        return redirect(new_thread.url())

    threads_query = (
        db.session.query(ForumThread)
        .filter(ForumThread.board_id == board.id)
        .order_by(ForumThread.is_pinned.desc(), ForumThread.date_modified.desc())
    )

    pagination = Pagination(per_page=THREADS_PER_PAGE, query=threads_query)

    return render_template("board.html", form=form, board=board, pagination=pagination)


def forums_thread(thread_id):
    thread_id = int(thread_id)
    form = ForumPostForm(request.form)

    thread = db.session.query(ForumThread).filter(ForumThread.id == thread_id).one_or_none()

    if not thread:
        return render_template('404.html'), 404

    if form.validate_on_submit():
        author = g.user.id
        body = request.form.get('body')
        new_post = ForumPost(author_id=author, thread_id=thread_id, body=body)
        db.session.add(new_post)
        db.session.commit()
        return redirect("forums/thread/" + str(thread_id) + "/")

    page_number = request.args.get('page', 1)
    page_number = int(page_number)

    post_query = (
        db.session.query(ForumPost)
        .filter(ForumPost.thread_id == thread_id)
        .order_by(ForumPost.date_created)
    )

    pagination = Pagination(per_page=POSTS_PER_PAGE, query=post_query)

    other_boards = db.session.query(Board).all()

    return render_template("thread.html", form=form, thread=thread,
            pagination=pagination, other_boards=other_boards)


@moderation_access_required
def forums_thread_move(thread_id):
    thread_id = int(thread_id)
    thread = db.session.query(ForumThread).filter(ForumThread.id == thread_id).one_or_none()

    if not thread:
        return render_template('404.html'), 404

    if 'move' in request.form:
        destination = int(request.form.get('destination'))
        thread.board_id = destination
        db.session.commit()
        flash("Thread moved successfully!")
        return redirect(thread.url())
