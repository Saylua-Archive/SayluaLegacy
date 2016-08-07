from saylua import app
from flask import (render_template, redirect,
                   url_for, flash, session, abort, request)

@app.route('/shelf/')
def book_shelf():
    return render_template("books/shelf.html")

@app.route('/read/<int:book_id>/')
def book_read(book_id):
    return render_template("books/read.html")
