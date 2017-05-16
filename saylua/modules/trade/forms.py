from saylua import app

from flask_wtf import FlaskForm
from wtforms import validators
from saylua.utils.form import sl_validators, UserCheck
from saylua.utils.form.fields import SlField, SlIntegerField


# This stores the user object from validation for further usage.
recipient_check = UserCheck()


class BankTransferForm(FlaskForm):
    recipient = SlField('Recipient Name', [
        sl_validators.Required(),
        sl_validators.NotBlank(),
        sl_validators.Min(app.config['MIN_USERNAME_LENGTH']),
        sl_validators.Max(app.config['MAX_USERNAME_LENGTH']),
        sl_validators.Username(),
        recipient_check.UsernameExists])
    cloud_coins = SlIntegerField('Cloud Coins', [
        validators.Optional(),
        sl_validators.NotNegative()])
    star_shards = SlIntegerField('Star Shards', [
        validators.Optional(),
        sl_validators.NotNegative()])
