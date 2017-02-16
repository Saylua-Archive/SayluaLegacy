from flask import render_template, request


def site_search():
    query = request.args.get('q')
    return render_template('results.html', query=query)
