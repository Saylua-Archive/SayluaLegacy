from saylua import app
from saylua.utils import is_devserver

from flask import render_template

import requests


def send_email(to, subject, text, html=None):
    # AppEngine SDK doesn't work with requests...
    if is_devserver():
        return None
    return requests.post(
        "https://api.mailgun.net/v3/mg.saylua.com/messages",
        auth=("api", app.config.get('MAILGUN_API_KEY')),
        data={"from": app.config.get('AUTOSEND_EMAIL'),
              "to": to,
              "subject": subject,
              "text": text,
              "html": html})


def send_confirmation_email(user, code=None):
    if not code:
        code = user.make_email_confirmation_code()

    url = app.config.get('MAIN_URL_ROOT') + code.url()

    to = [user.email]
    subject = "Confirm your Saylua account, %s" % user.name
    text = render_template('email/email_confirmation.txt', name=user.name, url=url)
    html = render_template('email/email_confirmation.html', name=user.name, url=url)
    return send_email(to, subject, text=text, html=html)
