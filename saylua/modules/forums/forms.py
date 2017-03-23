from wtforms import Form
from saylua.utils.form import sl_validators
from saylua.utils.form.fields import SlField, SlTextAreaField


class ForumThreadForm(Form):
    title = SlField('Thread Title', [
        sl_validators.Required(),
        sl_validators.NotBlank(),
        sl_validators.Min(3)])
    body = SlTextAreaField('Thread Body', [
        sl_validators.Required(),
        sl_validators.NotBlank(),
        sl_validators.Min(2)])


class ForumPostForm(Form):
    body = SlTextAreaField('Post Content', [
        sl_validators.Required(),
        sl_validators.NotBlank(),
        sl_validators.Min(2)])
