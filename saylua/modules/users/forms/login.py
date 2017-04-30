from saylua import app
from wtforms import Form
from flask_wtf.recaptcha import RecaptchaField, Recaptcha
from saylua.utils.form import sl_validators, UserCheck
from saylua.utils.form.fields import SlField, SlPasswordField, SlBooleanField

login_check = UserCheck()


class LoginForm(Form):
    username_or_email = SlField('Username/Email', [
        sl_validators.Required(),
        sl_validators.UsernameOrEmail(),
        login_check.UsernameOrEmailExists])
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
        sl_validators.Max(app.config['MAX_PASSWORD_LENGTH'])
    ])
    confirm_password = SlPasswordField('Confirm Password', [
        sl_validators.Required(),
        sl_validators.EqualTo('password', message='Passwords must match.')
    ])
    invite_code = SlField('Invite Code', [
        sl_validators.Required()])
    at_least_13 = SlBooleanField(
        'I certify that I am at least 13 years old.',
        [sl_validators.Required(message='You must be at least 13 to join Saylua.')])
    accept_tos = SlBooleanField(
        'I agree to the <a href="/terms/" target="_blank">Terms of Service</a>',
        [sl_validators.Required(message='You must agree to the Terms of Service!')])
    recaptcha = RecaptchaField(validators=[Recaptcha(message='Please check the CAPTCHA.')])


class RecoveryForm(Form):
    username_or_email = SlField('Username/Email', [
        sl_validators.Required(),
        sl_validators.UsernameOrEmail(),
        login_check.UsernameOrEmailExists])
    recaptcha = RecaptchaField(validators=[Recaptcha(message='Please check the CAPTCHA.')])


class PasswordResetForm(Form):
    password = SlPasswordField('New Password', [
        sl_validators.Required(),
        sl_validators.Min(app.config['MIN_PASSWORD_LENGTH']),
        sl_validators.Max(app.config['MAX_PASSWORD_LENGTH'])
    ])
    confirm_password = SlPasswordField('Confirm Password', [
        sl_validators.EqualTo('password', message='Passwords must match.')
    ])
