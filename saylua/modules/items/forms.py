from wtforms import Form
from saylua.utils.form import sl_validators
from saylua.utils.form.fields import SlField, SlTextAreaField


class ItemUploadForm(Form):
    name = SlField('Item Name', [
        sl_validators.Required(),
        sl_validators.NotBlank()])
    image_url = SlField('Image URL', [
        sl_validators.Required(),
        sl_validators.NotBlank()])
    description = SlTextAreaField('Description', [
        sl_validators.Required(),
        sl_validators.NotBlank()])
