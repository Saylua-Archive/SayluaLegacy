from flask import render_template, redirect, g


def home():
    if g.user:
        return redirect('/news/', code=302)
    return render_template("landing.html")


def news():
    return render_template("news.html")
