from saylua import app, admin_access_required
from flask import render_template, redirect, g, flash, request
from google.appengine.ext import ndb
from saylua.utils import urlize
import math

from saylua.models.forum import Board, BoardCategory, ForumThread, ForumPost
from google.appengine.datastore.datastore_query import Cursor
THREADS_PER_PAGE = 10
POSTS_PER_PAGE = 10


@app.route('/admin/forums/newcategory/', methods=['GET', 'POST'])
@admin_access_required
def new_board_category():
    if request.method == 'POST':
        category = request.form.get('category')
        new_category = BoardCategory(title=category)
        new_category.put()
        flash("New category: " + category + " successfully created.")
    return render_template("/admin/forums/newcategory.html")


@app.route('/admin/forums/newboard/', methods=['GET', 'POST'])
@admin_access_required
def new_board():
    categories = BoardCategory.query().fetch()
    if request.method == 'POST':
        title = request.form.get('title')
        category = request.form.get('category')
        description = request.form.get('description')
        url_title = urlize(title)
        new_board = Board(title=title, url_title=url_title,
                category_key=category, description=description)
        new_board.put()
        flash("New board: \"" + title + "\" successfully created!")
    return render_template("/admin/forums/newboard.html", categories=categories)


@app.route('/forums/')
def forums_home():
    categories = BoardCategory.query().fetch()
    blocks = []
    for category in categories:
        block = []
        block.append(category.title)
        boards = Board.query(Board.category_key==category.key.urlsafe()).fetch()
        block.append(boards)
        blocks.append(block)
    return render_template("forums/main.html", forum_blocks=blocks)


@app.route('/forums/board/<board_id>/', methods=['GET', 'POST'])
def forums_board(board_id):
    boards = Board.query(Board.url_title==board_id).fetch()
    if len(boards) != 1:
        return render_template('404.html'), 404
    else:
        board = boards[0]
        if request.method == 'POST':
            title = request.form.get('title')
            body = request.form.get('body')
            creator_key = g.user.key.urlsafe()
            board_id = board.key.id()
            new_thread = ForumThread(title=title, creator_key=creator_key,
                    board_id=board_id)
            thread_key = new_thread.put()
            thread_id = thread_key.id()
            url_title = board.url_title
            new_post = ForumPost(creator_key=creator_key, thread_id=thread_id,
                    board_id=board_id, body=body)
            new_post.put()
            return redirect("/forums/board/" + url_title + "/")
        page_number = request.args.get('page')
        if page_number is None:
            page_number = 1

        page_number = int(page_number)
        thread_query = ForumThread.query(ForumThread.board_id==board.key.id()).order(
            -ForumThread.is_pinned, -ForumThread.last_action)
        threads = thread_query.fetch(limit=THREADS_PER_PAGE,
            offset=((page_number - 1) * THREADS_PER_PAGE))

        total_threads = len(thread_query.fetch(keys_only=True))
        page_count = int(math.ceil(total_threads / float(THREADS_PER_PAGE)))
    return render_template("forums/board.html", board=board, threads=threads, page_count=page_count)


@app.route('/forums/thread/<thread_id>/', methods=['GET', 'POST'])
def forums_thread(thread_id):
    thread_id = int(thread_id)
    thread = ndb.Key(ForumThread, thread_id).get()
    if thread is None:
        return render_template('404.html'), 404
    board = ndb.Key(Board, thread.board_id).get()
    if request.method == 'POST':
        if 'move' in request.form:
            destination = int(request.form.get('destination'))
            thread.board_id = destination
            thread.put()
            post_query = ForumPost.query(ForumPost.thread_id==thread_id)
            posts = post_query.fetch()
            for post in posts:
                post.board_id = destination
                post.put()
            flash("Thread moved successfully!")
            return redirect("forums/thread/" + str(thread_id) + "/")
        else:
            creator_key = g.user.key.urlsafe()
            body = request.form.get('body')
            board_id = board.key.id()
            new_post = ForumPost(creator_key=creator_key, thread_id=thread_id,
                    board_id=board_id, body=body)
            new_post.put()
            thread.put()
            return redirect("forums/thread/" + str(thread_id) + "/")

    page_number = request.args.get('page')
    if page_number is None:
        page_number = 1
    page_number = int(page_number)
    post_query = ForumPost.query(ForumPost.thread_id==thread_id).order(ForumPost.created_time)
    posts = post_query.fetch(limit=POSTS_PER_PAGE,
            offset=((page_number - 1) * POSTS_PER_PAGE))
    page_count = int(math.ceil(len(post_query.fetch(keys_only=True))/float(POSTS_PER_PAGE)))
    other_boards = Board.query().fetch()
    return render_template("forums/thread.html", board=board, thread=thread, posts=posts,
            page_count=page_count, other_boards=other_boards)
