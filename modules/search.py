from flask import (Blueprint, render_template, redirect,
                   url_for, flash, session, abort, request)

search_module = Blueprint('search_module', __name__, url_prefix='/search')


@search_module.route("/", methods=['GET'])
def search():
    return render_template("search.html")
