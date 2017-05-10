from ..forms.login import RecoveryForm, login_check
from saylua.utils.email import send_email

from flask import render_template, request, flash


def recover_login():
    form = RecoveryForm(request.form)
    if request.method == 'POST' and form.validate():
        user = login_check.user
        code = user.make_password_reset_code()

        send_email(user.email, 'Saylua Password Reset',
            'Your password reset link is: ' + code.url())

        flash('Recovery email sent! Check the email address on file for the next step.')

    return render_template('login/recover.html', form=form)


def reset_password(user, code):
    return render_template('login/recover.html')
