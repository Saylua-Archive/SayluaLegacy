from saylua import app
from wtforms import Form
from saylua.utils.form import sl_validators, UserCheck
from saylua.utils.form.fields import SlField, SlTextAreaField

recipient_check = UserCheck()


class ConversationForm(Form):
    recipient = SlField('Recipient Name', [
        sl_validators.Required(),
        sl_validators.NotBlank(),
        sl_validators.Min(app.config['MIN_USERNAME_LENGTH']),
        sl_validators.Max(app.config['MAX_USERNAME_LENGTH']),
        sl_validators.Username(),
        recipient_check.UsernameExists])
    title = SlField('Message Title', [
        sl_validators.Required(),
        sl_validators.NotBlank(),
        sl_validators.Min(2)])
    text = SlTextAreaField('Message Text', [
        sl_validators.Required(),
        sl_validators.NotBlank(),
        sl_validators.Min(2)])


class ConversationReplyForm(Form):
    text = SlTextAreaField('Reply', [
        sl_validators.Required(),
        sl_validators.NotBlank(),
        sl_validators.Min(2)])
