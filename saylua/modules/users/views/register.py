from saylua import app, db

from saylua.models.user import LoginSession, User

from ..forms.register import RegisterForm, register_check

from flask import render_template, redirect, make_response, request, flash

import datetime


# Registration form shown to the user
def register():
    if app.config.get('REGISTRATION_DISABLED'):
        flash('Sorry, registration is currently disabled. Check back later!', 'error')
        return redirect('/login')
    form = RegisterForm(request.form)

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
        return resp

    return render_template('login/register.html', form=form)
