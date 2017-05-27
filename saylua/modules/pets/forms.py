from saylua import app
from flask_wtf import FlaskForm
from saylua.utils.form import sl_validators
from saylua.utils.form.fields import SlField, SlTextAreaField


class PetEditForm(FlaskForm):
    name = SlField('Name', [
        sl_validators.Required(),
        sl_validators.NotBlank(),
        sl_validators.Max(app.config['MAX_PET_NAME_LENGTH'])])
    description = SlTextAreaField('Description')
    pronouns = SlField('Pronouns', [
        sl_validators.Max(app.config['MAX_PET_NAME_LENGTH'])])
