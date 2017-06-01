from flask_wtf import FlaskForm
from saylua.utils.form import sl_validators
from saylua.utils.form.fields import SlField, SlIntegerField, SlBooleanField

from wtforms import validators


class BanForm(FlaskForm):
    days = SlIntegerField('Days Banned', [validators.Optional()])
    is_permanent = SlBooleanField('Ban this user permanently?')
    reason = SlField('Ban Reason', [sl_validators.Required()])


class MuteForm(FlaskForm):
    days = SlIntegerField('Days Muted', [validators.Optional()])
    is_permanent = SlBooleanField('Mute this user permanently?')
    reason = SlField('Mute Reason', [sl_validators.Required()])
