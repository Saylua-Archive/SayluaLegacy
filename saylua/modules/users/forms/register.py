from saylua import app

from flask_wtf import FlaskForm
from flask_wtf.recaptcha import RecaptchaField, Recaptcha
from saylua.utils.form import sl_validators, UserCheck
from saylua.utils.form.fields import SlField, SlPasswordField, SlBooleanField

register_check = UserCheck()


class RegisterForm(FlaskForm):
    username = SlField('Username', [
        sl_validators.Required(),
        sl_validators.Min(app.config['MIN_USERNAME_LENGTH']),
        sl_validators.Max(app.config['MAX_USERNAME_LENGTH']),
        sl_validators.Username(),
        sl_validators.UsernameUnique()])
    email = SlField('Email Address', [
        sl_validators.Required(),
        sl_validators.Email(),
        sl_validators.EmailUnique()])
    password = SlPasswordField('Password', [
        sl_validators.Required(),
        sl_validators.Min(app.config['MIN_PASSWORD_LENGTH']),
        sl_validators.Max(app.config['MAX_PASSWORD_LENGTH'])
    ])
    confirm_password = SlPasswordField('Confirm Password', [
        sl_validators.Required(),
        sl_validators.EqualTo('password', message='Passwords must match.')
    ])
    invite_code = SlField('Invite Code', [
        sl_validators.Required(),
        register_check.InviteCodeValid])
    at_least_13 = SlBooleanField(
        'I certify that I am at least 13 years old.',
        [sl_validators.Required(message='You must be at least 13 to join Saylua.')])
    accept_tos = SlBooleanField(
        'I agree to the <a href="/terms/" target="_blank" rel="noopener">Terms of Service</a>',
        [sl_validators.Required(message='You must agree to the Terms of Service!')])
    recaptcha = RecaptchaField(validators=[Recaptcha(message='Please check the CAPTCHA.')])
