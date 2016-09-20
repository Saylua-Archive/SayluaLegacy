from saylua import app
from flask import (render_template, redirect,
                   url_for, flash, session, abort, request)
from google.appengine.ext import ndb

from saylua.models.forum import Board, BoardCategory, ForumThread, ForumPost

@app.route('/forums/newcategory', methods=['POST'])
def new_category_post():
    category = request.form['category']
    return render_template("forums/main.html")

@app.route('/forums/newcategory', methods=['GET'])
def new_category_view():
    return render_template("forums/newcategory.html")

@app.route('/forums/newboard', methods=['POST'])
def new_board():
    category = request.form['title']
    return render_template("forums/main.html")

@app.route('/forums/')
def forums_home():
    return render_template("forums/main.html")

@app.route('/forums/board/<board_id>/')
def forums_board(board_id):
    return render_template("forums/board.html")

@app.route('/forums/thread/<thread_id>/')
def forums_thread(thread_id):
    return render_template("forums/thread.html")
