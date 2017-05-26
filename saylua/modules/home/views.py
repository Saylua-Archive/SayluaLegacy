from flask import render_template, redirect, g

from saylua import db, app
from saylua.utils import is_devserver
from saylua.modules.forums.models.db import ForumThread, Board

import random


def home():
    try:
        if is_devserver() or g.user:
            return redirect('/news/', code=302)
        return landing()
    except AttributeError:
        return landing()


def landing():
    return render_template("landing.html")


def news():
    news_canon_name = app.config.get('NEWS_BOARD_CANON_NAME')
    threads = db.session.query(ForumThread).join(ForumThread.board).filter(
        Board.canon_name == news_canon_name).order_by(
        ForumThread.date_created.desc())
    return render_template("newspaper/news.html", threads=threads,
        news_canon_name=news_canon_name)


def puzzle():
    puzzle = generate_puzzle()

    return render_template("newspaper/puzzle.html", puzzle=puzzle)


# Generate a 9x9 puzzle that meets the game constraints and is solvable using
# backtracing.
# This is essentially a puzzle solver which solves randomly and stops partway through.
def generate_puzzle():
    puzzle = [[0] * 9 for _ in range(9)]

    def puzzle_step(filled=0):
        # Get next square to fill.
        i, j = divmod(filled, 9)

        numbers = list(range(1, 10))
        random.shuffle(numbers)
        for k in numbers:
            puzzle[i][j] = k

            # TODO: puzzle_meets_constraints checks the whole board. We can
            # check only the number we added.
            if puzzle_meets_contraints(puzzle):
                if filled + 1 >= 9 * 9 or puzzle_step(filled + 1):
                    return puzzle

        # If none of the possible numbers returns true, this is a dead end.
        puzzle[i][j] = 0
        return None

    puzzle = puzzle_step()

    # Remove squares from the filled board to generate a puzzle.
    for _ in range(81 / 3 * 2):
        i = random.randint(0, 8)
        j = random.randint(0, 8)
        puzzle[i][j] = 0

    return puzzle


# Takes in a 9x9 puzzle and checks to see if the game constraints are met.
# Note that blank squares are not checked.
def puzzle_meets_contraints(puzzle):
    for i in range(9):
        rowSet = {}
        colSet = {}
        boxSet = {}
        for j in range(9):
            # Check rows.
            rNum = puzzle[i][j]
            if rNum:
                if rNum in rowSet:
                    return False
                rowSet[puzzle[i][j]] = True

            # Check columns.
            cNum = puzzle[j][i]
            if cNum:
                if cNum in colSet:
                    return False
                colSet[cNum] = True

            # Check boxes, those 3x3 board subsections. (ith box, jth entry in box.)
            # Sorry, this math is a little confusing.
            bNum = puzzle[(i / 3) * 3 + j / 3][(i % 3) * 3 + j % 3]
            if bNum:
                if bNum in boxSet:
                    return False
                boxSet[bNum] = True

    return True
