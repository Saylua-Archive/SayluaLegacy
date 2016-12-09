from saylua import app
from flask import render_template


def book_shelf():
    return render_template("shelf.html")


def book_read(book_id):
    return render_template("read.html")
