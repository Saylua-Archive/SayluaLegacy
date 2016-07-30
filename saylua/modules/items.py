from saylua import app
from flask import (render_template, redirect,
                   url_for, flash, session, abort, request)

@app.route('/inventory/')
def items_inventory():
    return render_template("items/inventory.html")
