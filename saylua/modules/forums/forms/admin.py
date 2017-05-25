from flask_wtf import FlaskForm
from wtforms.fields import SelectField

from saylua.utils.form import sl_validators
from saylua.utils.form.fields import SlField, SlTextAreaField, SlBooleanField


class ForumBoardForm(FlaskForm):
    title = SlField('Board Title', [
        sl_validators.Required(),
        sl_validators.NotBlank(),
        sl_validators.Min(3)])
    description = SlTextAreaField('Board Description', [
        sl_validators.Required(),
        sl_validators.NotBlank(),
        sl_validators.Min(2)])
    category = SelectField('Category', coerce=int)
    order = SlField('Sort Order')

    is_news = SlBooleanField('Make threads posted here news')
    moderators_only = SlBooleanField('Restrict this board to moderators')
