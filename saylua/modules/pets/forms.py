from flask_wtf import FlaskForm
from saylua.utils.form import sl_validators
from saylua.utils.form.fields import SlField


class ItemUploadForm(FlaskForm):
    name = SlField('Name', [
        sl_validators.Required(),
        sl_validators.NotBlank()])
