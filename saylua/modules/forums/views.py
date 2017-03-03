from flask import render_template, redirect, g, flash, request
import flask_sqlalchemy
from saylua import db

from .models.db import Board, BoardCategory, ForumThread, ForumPost


THREADS_PER_PAGE = 10
POSTS_PER_PAGE = 10


def forums_home():
    categories = db.session.query(BoardCategory).all()
    return render_template("main.html", categories=categories)


def forums_board(board_slug):
    try:
        board = db.session.query(Board).filter(Board.url_slug == board_slug).one()

        if request.method == 'POST':
            title = request.form.get('title')
            body = request.form.get('body')
            author = g.user.id
            board_id = board.id
            url_title = post_new_thread(title, body, author, board_id, board)
            return redirect("/forums/board/" + url_title + "/")

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

        page_count = threads_query.count() // THREADS_PER_PAGE

        return render_template("board.html", board=board, threads=threads, page_count=page_count)

    except (flask_sqlalchemy.orm.exc.MultipleResultsFound, flask_sqlalchemy.orm.exc.NoResultFound):
        return render_template('404.html'), 404


def post_new_thread(title, body, creator_key, board_id, board=None):
    if board is None:
        board = Board.query(Board.url_title == board_id).fetch()[0]
    new_thread = ForumThread(title=title, creator_key=creator_key, board_id=board_id)
    thread_key = new_thread.put()
    thread_id = thread_key.id()
    url_title = board.url_title
    new_post = ForumPost(creator_key=creator_key, thread_id=thread_id, board_id=board_id, body=body)
    new_post.put()
    return url_title


def forums_thread(thread_id):
    thread_id = int(thread_id)

    try:
        thread = db.session.query(ForumThread).filter(ForumThread.id == thread_id).one()
        board = thread.board

        if request.method == 'POST':
            if 'move' in request.form:
                destination = int(request.form.get('destination'))
                thread.board_id = destination
                thread.put()
                post_query = ForumPost.query(ForumPost.thread_id == thread_id)
                posts = post_query.fetch()
                for post in posts:
                    post.board_id = destination
                    post.put()
                flash("Thread moved successfully!")
                return redirect("forums/thread/" + str(thread_id) + "/")
            else:
                creator_key = g.user.id.urlsafe()
                body = request.form.get('body')
                board_id = board.key.id()
                new_post = ForumPost(creator_key=creator_key, thread_id=thread_id,
                        board_id=board_id, body=body)
                new_post.put()
                thread.put()
                return redirect("forums/thread/" + str(thread_id) + "/")

        page_number = request.args.get('page', 1)
        page_number = int(page_number)

        post_query = (
            db.session.query(ForumPost)
            .filter(ForumPost.thread_id == thread_id)
            .order_by(ForumPost.date_created.desc())
        )

        posts = (
            post_query
            .limit(POSTS_PER_PAGE)
            .offset((page_number - 1) * POSTS_PER_PAGE)
        )

        page_count = post_query.count() // POSTS_PER_PAGE
        other_boards = db.session.query(Board).all()

        return render_template("thread.html", board=board, thread=thread, posts=posts,
                page_count=page_count, other_boards=other_boards)

    except (flask_sqlalchemy.orm.exc.MultipleResultsFound, flask_sqlalchemy.orm.exc.NoResultFound):
        return render_template('404.html'), 404
