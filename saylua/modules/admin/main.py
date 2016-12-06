from saylua import app
from saylua.wrappers import admin_access_required

from flask import render_template


@app.route('/admin/', methods=['GET'])
@admin_access_required
def admin_panel():
    return render_template('admin/main.html')