from saylua import app, login_required
from flask import (render_template, redirect, make_response,
                   url_for, flash, session, abort, request, g)

@app.route('/admin/', methods=['GET'])
def admin_panel():
    return render_template('admin/main.html')
