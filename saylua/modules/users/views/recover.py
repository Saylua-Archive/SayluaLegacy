from ..forms.login import RecoveryForm

from flask import render_template, request


def recover_login():
    form = RecoveryForm(request.form)
    return render_template('login/recover.html', form=form)


def reset_password(user, code):
    return render_template('login/recover.html')
