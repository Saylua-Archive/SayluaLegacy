from saylua.wrappers import admin_access_required

from flask import render_template


@admin_access_required()
def admin_panel():
    return render_template('main.html')
