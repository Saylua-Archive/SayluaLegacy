from flask import render_template, redirect, g, flash, request
import flask_sqlalchemy
from saylua import db
from saylua.utils import urlize

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
            url_title = urlize(board.title)
            new_thread = ForumThread(title=title, author=author, board_id=board_id)
            db.session.add(new_thread)
            db.session.flush()
            new_post = ForumPost(author=author, thread_id=new_thread.id, body=body)
            db.session.add(new_post)
            db.session.commit()
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


def forums_thread(thread_id):
    thread_id = int(thread_id)

    try:
        thread = db.session.query(ForumThread).filter(ForumThread.id == thread_id).one()
        board = thread.board

        if request.method == 'POST':
            if 'move' in request.form:
                destination = int(request.form.get('destination'))
                thread.board_id = destination
                db.session.commit()
                flash("Thread moved successfully!")
                return redirect("forums/thread/" + str(thread_id) + "/")
            else:
                author = g.user.id
                body = request.form.get('body')
                new_post = ForumPost(author=author, thread_id=thread_id, body=body)
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

        page_count = post_query.count() // POSTS_PER_PAGE
        other_boards = db.session.query(Board).all()

        return render_template("thread.html", board=board, thread=thread, posts=posts,
                page_count=page_count, other_boards=other_boards)

    except (flask_sqlalchemy.orm.exc.MultipleResultsFound, flask_sqlalchemy.orm.exc.NoResultFound):
        return render_template('404.html'), 404
