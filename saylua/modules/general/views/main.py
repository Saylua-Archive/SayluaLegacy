from flask import render_template, redirect, g, abort

from saylua.utils import is_devserver


def home():
    try:
        if is_devserver() or g.user:
            return redirect('/news/', code=302)
        return landing()
    except AttributeError:
        return landing()


def landing():
    return render_template("landing.html")


def view_page(template):
    template_name = "pages/" + template + ".html"

    try:
        return render_template(template_name)
    except:
        abort(404)


def banned():
    if not (g.logged_in and g.user.is_banned()):
        return render_template("404.html"), 404
    return render_template("banned.html")
