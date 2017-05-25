from flask_wtf import FlaskForm
from wtforms.fields import SelectField

from saylua.utils.form import sl_validators
from saylua.utils.form.fields import (SlField, SlTextAreaField, SlBooleanField,
    SlIntegerField)


class ForumBoardForm(FlaskForm):
    title = SlField('Board Title', [
        sl_validators.Required(),
        sl_validators.NotBlank(),
        sl_validators.Min(3)])
    canon_name = SlField('Canon Name', [
        sl_validators.Required(),
        sl_validators.NotBlank(),
        sl_validators.Min(3),
        sl_validators.CanonName()])
    description = SlTextAreaField('Board Description', [
        sl_validators.Required(),
        sl_validators.NotBlank(),
        sl_validators.Min(2)])
    category_id = SelectField('Category', coerce=int)
    order = SlIntegerField('Sort Order')

    moderators_only = SlBooleanField('Restrict this board to moderators')
