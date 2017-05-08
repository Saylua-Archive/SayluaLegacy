from saylua import app
import requests


def send_email(to, subject, text):
    return requests.post(
        "https://api.mailgun.net/v3/mg.saylua.com/messages",
        auth=("api", app.config.get('MAILGUN_API_KEY')),
        data={"from": app.config.get('AUTOSEND_EMAIL'),
              "to": to,
              "subject": subject,
              "text": text})


def send_confirmation_email(user, code=None):
    if not code:
        code = user.make_email_confirmation_code()

    url = app.config.get('MAIN_URL_ROOT') + code.url()

    to = [user.email]
    subject = "Confirm your Saylua account, %s" % user.name
    text = ("""You've registered a new account on Saylua. Please click the link
        below to verify your email: %s """ % url)
    return send_email(to, subject, text)
