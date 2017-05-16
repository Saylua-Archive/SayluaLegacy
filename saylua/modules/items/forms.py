from flask_wtf import FlaskForm
from saylua.utils.form import sl_validators
from saylua.utils.form.fields import SlField, SlFileField, SlTextAreaField


class ItemUploadForm(FlaskForm):
    name = SlField('Item Name', [
        sl_validators.Required(),
        sl_validators.NotBlank()])
    image = SlFileField('Image File', [
        sl_validators.Required(),
        sl_validators.EndsWith('.png', message='File type must be a PNG.')
    ])
    description = SlTextAreaField('Description', [
        sl_validators.Required(),
        sl_validators.NotBlank()])
