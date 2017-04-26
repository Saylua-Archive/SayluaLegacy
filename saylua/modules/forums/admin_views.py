from saylua import db

from saylua.wrappers import admin_access_required
from flask import render_template, flash, request
from saylua.utils import urlize

from .models.db import Board, BoardCategory


@admin_access_required
def new_board_category():
    if request.method == 'POST':
        category = request.form.get('category')
        new_category = BoardCategory(title=category)
        db.session.add(new_category)
        db.session.commit()
        flash("New category: " + category + " successfully created.")
    return render_template("admin/add_category.html")


@admin_access_required
def new_board():
    categories = db.session.query(BoardCategory).all()
    if request.method == 'POST':
        title = request.form.get('title')
        category = request.form.get('category')
        description = request.form.get('description')

        category = db.session.query(BoardCategory).get(category)

        url_title = urlize(title)
        new_board = Board(title=title, text_id=url_title,
                categories=[category], description=description)
        db.session.add(new_board)
        db.session.commit()

        flash("New board: \"" + title + "\" successfully created!")
    return render_template("admin/add_board.html", categories=categories)
