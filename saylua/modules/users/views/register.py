from saylua import app, db

from saylua.models.user import LoginSession, User
from saylua.utils import get_from_request
from saylua.utils.email import send_confirmation_email

from ..forms.register import RegisterForm, register_check

from flask import render_template, redirect, make_response, request, flash, g

import datetime


# Registration form shown to the user
def register():
    if app.config.get('REGISTRATION_DISABLED'):
        flash('Sorry, registration is currently disabled. Check back later!', 'error')
        return redirect('/login')
    form = RegisterForm(request.form)
    form.invite_code.data = get_from_request(request, 'invite_code')

    if not app.config.get('INVITE_ONLY'):
        del form.invite_code

    if request.method == 'POST' and form.validate():
        username = form.username.data
        password = form.password.data
        email = form.email.data

        phash = User.hash_password(password)
        new_user = User(
            username=username,
            phash=phash,
            email=email
        )

        db.session.add(new_user)
        db.session.commit()

        if app.config.get('INVITE_ONLY'):
            # Claim the user's invite code if one was used.
            invite_code = register_check.invite_code

            # Note that an invite code should exist assuming the form validation
            # passed... If an empty code gets here, we have a problem.
            invite_code.recipient_id = new_user.id
            db.session.add(invite_code)

        # Add a session to the datastore
        expires = datetime.datetime.utcnow()
        expires += datetime.timedelta(days=app.config['COOKIE_DURATION'])
        new_session = LoginSession(user_id=new_user.id, expires=expires)

        db.session.add(new_session)
        db.session.commit()

        # Generate a matching cookie and redirct
        resp = make_response(redirect('/'))
        resp.set_cookie('session_id', new_session.id, expires=expires)
        resp.set_cookie('user_id', str(new_user.id), expires=expires)

        # Send the confirmation email for the new account.
        send_confirmation_email(new_user)
        return resp

    return render_template('login/register.html', form=form)


# The endpoint to confirm email addresses.
def register_email():
    if g.logged_in and not g.user.email_confirmed and request.method == 'POST':
        send_confirmation_email(g.user)
        return 'Confirmation email sent'

    # Note that users do not have to be logged in to confirm an email address.
    return 'Hello'
