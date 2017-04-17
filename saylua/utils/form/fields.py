from wtforms import (BooleanField, StringField, PasswordField,
    TextAreaField, IntegerField, FileField)

from widgets import (SlInput, SlPasswordInput, SlCheckboxInput, SlTextArea,
    SlNumberInput, SlFileInput)


class SlField(StringField):
    widget = SlInput()


class SlFileField(FileField):
    widget = SlFileInput()


class SlPasswordField(PasswordField):
    widget = SlPasswordInput()


class SlBooleanField(BooleanField):
    widget = SlCheckboxInput()


class SlTextAreaField(TextAreaField):
    widget = SlTextArea()


class SlIntegerField(IntegerField):
    widget = SlNumberInput()
