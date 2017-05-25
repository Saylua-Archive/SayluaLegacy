from saylua import db

from saylua.wrappers import admin_access_required
from flask import render_template, flash, request
from saylua.utils import canonize

from .forms.admin import ForumBoardForm
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
def manage_boards():
    form = ForumBoardForm(request.form)
    categories = db.session.query(BoardCategory).all()
    form.category.choices = [(c.id, c.title) for c in categories]
    if form.validate_on_submit():
        title = form.title.data
        category = form.category.data
        description = form.description.data
        is_news = form.is_news.data
        moderators_only = form.moderators_only

        category = db.session.query(BoardCategory).get(category)

        canon_name = canonize(title)

        if not canon_name or Board.by_canon_name(canon_name):
            flash("Board name is too similar to an existing board.", 'error')
        else:
            new_board = Board(title=title, canon_name=canon_name,
                categories=[category], description=description, is_news=is_news,
                moderators_only=moderators_only)
            db.session.add(new_board)
            db.session.commit()

            flash("New board: \"" + title + "\" successfully created!")
    return render_template("admin/boards.html", form=form, categories=categories)


@admin_access_required
def edit_board(canon_name):
    board = Board.by_canon_name(canon_name)
    form = ForumBoardForm(request.form, obj=board)
    categories = db.session.query(BoardCategory).all()
    form.category.choices = [(c.id, c.title) for c in categories]

    return render_template("admin/board_edit.html", form=form)
