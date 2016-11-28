from saylua import app
from flask import render_template, redirect


@app.route('/')
def home():
    logged_in = False
    if logged_in:
        return redirect('/news/', code=302)
    return render_template("home/landing.html")


@app.route('/news/')
def home_news():
    return render_template("home/news.html")
