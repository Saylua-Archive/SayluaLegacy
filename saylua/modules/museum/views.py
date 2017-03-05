from flask import render_template


def museum_main():
    return render_template("museum.html")


def book_shelf():
    return render_template("shelf.html")


def book_read(book_id):
    return render_template("read.html")
