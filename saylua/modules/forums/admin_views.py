from saylua.wrappers import admin_access_required
from flask import render_template, flash, request
from saylua.utils import urlize

from .models.db import Board, BoardCategory


@admin_access_required
def new_board_category():
    if request.method == 'POST':
        category = request.form.get('category')
        add_board_category(category)
        flash("New category: " + category + " successfully created.")
    return render_template("admin/newcategory.html")


def add_board_category(title):
    new_category = BoardCategory(title=title)
    new_category.put()


@admin_access_required
def new_board():
    categories = BoardCategory.query().fetch()
    if request.method == 'POST':
        title = request.form.get('title')
        category = request.form.get('category')
        description = request.form.get('description')
        add_new_board(title, category, description)
        flash("New board: \"" + title + "\" successfully created!")
    return render_template("admin/newboard.html", categories=categories)


def add_new_board(title, category, description):
    url_title = urlize(title)
    new_board = Board(title=title, url_title=url_title,
            category_key=category, description=description)
    new_board.put()
