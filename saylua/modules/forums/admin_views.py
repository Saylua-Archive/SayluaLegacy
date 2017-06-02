from saylua import db

from saylua.wrappers import admin_access_required
from flask import render_template, flash, request

from sqlalchemy.exc import IntegrityError

from .forms.admin import ForumBoardForm, ForumCategoryForm
from .models.db import Board, BoardCategory


@admin_access_required()
def manage_categories():
    form = ForumCategoryForm(request.form)
    if form.validate_on_submit():
        category = BoardCategory()
        form.populate_obj(category)
        db.session.add(category)
        db.session.commit()
        flash("New category: " + category.title + " successfully created.")

    categories = BoardCategory.get_categories()

    return render_template("admin/categories.html", categories=categories,
        form=form)


@admin_access_required()
def edit_category(canon_name):
    category = BoardCategory.by_canon_name(canon_name)
    form = ForumCategoryForm(request.form, obj=category)
    if form.validate_on_submit():
        form.populate_obj(category)
        db.session.add(category)
        db.session.commit()
        flash("Category successfully edited.")
    return render_template("admin/category_edit.html", form=form)


@admin_access_required()
def manage_boards():
    form = ForumBoardForm(request.form)
    categories = BoardCategory.get_categories()
    form.category_id.choices = [(c.id, c.title) for c in categories]
    if form.validate_on_submit():
        new_board = Board()
        form.populate_obj(new_board)

        try:
            db.session.add(new_board)
            db.session.commit()

            flash("New board: \"" + new_board.title + "\" successfully created!")
        except IntegrityError:
            flash("Board canon name already exists!", "error")

    return render_template("admin/boards.html", form=form, categories=categories)


@admin_access_required()
def edit_board(canon_name):
    board = Board.by_canon_name(canon_name)
    form = ForumBoardForm(request.form, obj=board)
    categories = BoardCategory.get_categories()
    form.category_id.choices = [(c.id, c.title) for c in categories]

    if form.validate_on_submit():
        form.populate_obj(board)

        db.session.add(board)
        db.session.commit()

        flash("You've updated the board: " + board.title)

    return render_template("admin/board_edit.html", form=form)
