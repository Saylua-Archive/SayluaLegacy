from saylua import app
from wtforms import Form
from flask_wtf.recaptcha import RecaptchaField, Recaptcha
from saylua.utils.form import sl_validators, UserCheck
from saylua.utils.form.fields import SlField, SlPasswordField, SlBooleanField

login_check = UserCheck()


class LoginForm(Form):
    username = SlField('Username', [
        sl_validators.Required(),
        sl_validators.Username(),
        login_check.UsernameExists])
    password = SlPasswordField('Password', [
        sl_validators.Required(),
        login_check.PasswordValid])


class RegisterForm(Form):
    username = SlField('Username', [
        sl_validators.Required(),
        sl_validators.Min(app.config['MIN_USERNAME_LENGTH']),
        sl_validators.Max(app.config['MAX_USERNAME_LENGTH']),
        sl_validators.Username(),
        sl_validators.UsernameUnique()])
    email = SlField('Email Address', [
        sl_validators.Required(),
        sl_validators.Email()])
    password = SlPasswordField('Password', [
        sl_validators.Required(),
        sl_validators.Min(app.config['MIN_PASSWORD_LENGTH']),
        sl_validators.Max(app.config['MAX_PASSWORD_LENGTH']),
        sl_validators.EqualTo('confirm_password', message='Passwords must match.')
    ])
    confirm_password = SlPasswordField('Confirm Password')
    accept_tos = SlBooleanField(
        'I agree to the <a href="/terms/" target="_blank">Terms of Service</a>',
        [sl_validators.Required(message='You must agree to the Terms of Service!')])
    recaptcha = RecaptchaField(validators=[Recaptcha(message='Please check the CAPTCHA.')])
