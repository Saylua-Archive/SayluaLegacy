from saylua import app
from flask import (render_template, redirect,
                   url_for, flash, session, abort, request)

@app.route('/search/')
def site_search():
    query = request.args.get('q')
    return render_template('search/results.html', query=query)
