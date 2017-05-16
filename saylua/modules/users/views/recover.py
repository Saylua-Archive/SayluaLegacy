from ..forms.login import RecoveryForm, PasswordResetForm, login_check

from saylua import db
from saylua.models.user import User, PasswordResetCode
from saylua.utils import is_devserver
from saylua.utils.email import send_email

from flask import render_template, request, flash, redirect


def recover_login():
    form = RecoveryForm(request.form)
    if form.validate_on_submit():
        user = login_check.user
        code = user.make_password_reset_code()

        if is_devserver():
            flash('DEBUG MODE: Your reset code is %s' % code.url())
        else:
            send_email(user.email, 'Saylua Password Reset',
                'Your password reset link is: ' + code.url())
            flash('Recovery email sent! Check the email address on file for the next step.')

    return render_template('login/recover.html', form=form)


def reset_password(user_id, code):
    code = db.session.query(PasswordResetCode).get((code, user_id))
    if not code or code.invalid():
        flash('The password reset code you have entered is invalid.', 'error')
        return redirect('/')

    form = PasswordResetForm(request.form)
    if form.validate_on_submit():
        user = db.session.query(User).get(user_id)
        user.password_hash = User.hash_password(form.password.data)
        code.used = True
        db.session.commit()
        flash('Your password has successfully been changed! Here, try logging in now.')
        return redirect('/login')

    return render_template('login/reset.html', form=form)
