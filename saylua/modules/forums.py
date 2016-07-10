from saylua import app
from flask import (render_template, redirect,
                   url_for, flash, session, abort, request)

@app.route('/forums/')
def forums_home():
    return render_template("forums/main.html")

@app.route('/forums/board/<int:board_id>/')
def forums_board(board_id):
    return render_template("forums/board.html")

@app.route('/forums/thread/<int:thread_id>/')
def forums_thread(thread_id):
    return render_template("forums/thread.html")
