from wtforms import (BooleanField, StringField, PasswordField,
    TextAreaField, IntegerField)

from widgets import (SlInput, SlPasswordInput, SlCheckboxInput, SlTextArea,
    SlNumberInput)


class SlField(StringField):
    widget = SlInput()


class SlPasswordField(PasswordField):
    widget = SlPasswordInput()


class SlBooleanField(BooleanField):
    widget = SlCheckboxInput()


class SlTextAreaField(TextAreaField):
    widget = SlTextArea()


class SlIntegerField(IntegerField):
    widget = SlNumberInput()
