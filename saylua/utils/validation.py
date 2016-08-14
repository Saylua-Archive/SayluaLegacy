from flask import flash
import re

class FieldValidator:
    def __init__(self, field, value):
        self.field_name = field
        self.input = value
        self.valid = True
        self.error = None

    def required(self, error=None):
        return self._validate(bool(self.input), error,
            self.field_name.title() + ' is required. ')

    def matches(self, input2, error=None):
        return self._validate(self.input == input2, error,
            self.field_name.title() + ' must match. ')

    def min(self, length, error=None):
        return self._validate(len(self.input) >= length, error,
            self.field_name.title() + ' must be at least ' + str(length) + ' characters')

    def max(self, length, error=None):
        return self._validate(len(self.input) <= length, error,
            self.field_name.title() + ' cannot be more than  ' + str(length) + ' characters')

    def matches_regex(self, regex, error=None):
        pattern = re.compile(regex)
        return self._validate(pattern.match(self.input), error,
            self.field_name.title() + ' is not formatted correctly. ')

    def is_valid(self):
        return self.valid

    def flash(self):
        if self.error:
            flash(self.error, 'error')

    def _validate(self, expression, error, default_error):
        if not error:
            error = default_error

        if not expression:
            if not self.error:
                self.error = error
            self.valid = False

        return self
