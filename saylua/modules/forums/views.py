from flask import render_template, redirect, g, flash, request
import flask_sqlalchemy
from saylua import db

from .models.db import Board, BoardCategory, ForumThread, ForumPost
from .forms import ForumThreadForm, ForumPostForm


THREADS_PER_PAGE = 10
POSTS_PER_PAGE = 10


def forums_home():
    categories = (db.session.query(BoardCategory)
        .order_by(BoardCategory.order.asc())
        .all())
    return render_template("forums_home.html", categories=categories)


def forums_board(canon_name):
    form = ForumThreadForm(request.form)
    try:
        board = db.session.query(Board).filter(Board.canon_name == canon_name).one()

        if form.validate_on_submit():
            title = request.form.get('title')
            body = request.form.get('body')
            author = g.user.id
            board_id = board.id
            new_thread = ForumThread(title=title, author_id=author, board_id=board_id)
            new_post = ForumPost(author_id=author, thread=new_thread, body=body)
            db.session.add(new_thread)
            db.session.add(new_post)
            db.session.commit()
            return redirect(board.url())

        page_number = request.args.get('page', 1)
        page_number = int(page_number)

        threads_query = (
            db.session.query(ForumThread)
            .filter(ForumThread.board_id == board.id)
            .order_by(ForumThread.is_pinned.desc(), ForumThread.date_modified.desc())
        )

        threads = (
            threads_query
            .limit(THREADS_PER_PAGE)
            .offset((page_number - 1) * THREADS_PER_PAGE)
            .all()
        )

        threads_count = (
            db.session.query(ForumThread)
            .filter(ForumThread.board_id == board.id)
            .count()
        )

        page_count = (THREADS_PER_PAGE + threads_count - 1) // THREADS_PER_PAGE

        return render_template("board.html", form=form,
            board=board, threads=threads, page_count=page_count)

    except (flask_sqlalchemy.orm.exc.MultipleResultsFound, flask_sqlalchemy.orm.exc.NoResultFound):
        return render_template('404.html'), 404


def forums_thread(thread_id):
    thread_id = int(thread_id)
    form = ForumPostForm(request.form)

    try:
        thread = db.session.query(ForumThread).filter(ForumThread.id == thread_id).one()
        board = thread.board

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

        posts = (
            post_query
            .limit(POSTS_PER_PAGE)
            .offset((page_number - 1) * POSTS_PER_PAGE)
        )

        posts_count = (
            db.session.query(ForumPost)
            .filter(ForumPost.thread_id == thread_id)
            .count()
        )

        page_count = (POSTS_PER_PAGE + posts_count - 1) // POSTS_PER_PAGE
        other_boards = db.session.query(Board).all()

        return render_template("thread.html", form=form, board=board, thread=thread,
                posts=posts, page_count=page_count, other_boards=other_boards)

    except (flask_sqlalchemy.orm.exc.MultipleResultsFound, flask_sqlalchemy.orm.exc.NoResultFound):
        return render_template('404.html'), 404


def forums_thread_move(thread_id):
    thread_id = int(thread_id)
    try:
        thread = db.session.query(ForumThread).filter(ForumThread.id == thread_id).one()
        if 'move' in request.form:
            destination = int(request.form.get('destination'))
            thread.board_id = destination
            db.session.commit()
            flash("Thread moved successfully!")
            return redirect(thread.url())
    except (flask_sqlalchemy.orm.exc.MultipleResultsFound, flask_sqlalchemy.orm.exc.NoResultFound):
        return render_template('404.html'), 404
