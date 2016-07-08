from flask import (Blueprint, render_template, redirect,
                   url_for, flash, session, abort, request)

import calendar, time
from PIL import Image
import datetime

submit_module = Blueprint('submit_module', __name__, url_prefix='/submit')

@submit_module.route("/")
def submit():
    return render_template("submit.html")

@submit_module.route("/", methods=['POST'])
def submit_post():
    data = request.files['file']
    if data:
        filename = str(calendar.timegm(time.gmtime())) + "_" + data.filename
        flash("Uploaded: " + data.filename)
    else:
        flash("No file uploaded! ")
    return render_template("submit.html")
