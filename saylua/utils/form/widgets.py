from wtforms import widgets

class SlInput(widgets.TextInput):
    def __init__(self, error_class='error'):
        self.error_class = error_class

    def __call__(self, field, **kwargs):
        if field.errors:
            c = kwargs.pop('class', '') or kwargs.pop('class_', '')
            kwargs['class'] = '%s %s' % (self.error_class, c)

        if not 'placeholder' in kwargs:
            kwargs['placeholder'] = field.label.text
        return super(SlInput, self).__call__(field, **kwargs)

class SlTextArea(widgets.TextArea):
    def __init__(self, error_class='error'):
        self.error_class = error_class

    def __call__(self, field, **kwargs):
        if field.errors:
            c = kwargs.pop('class', '') or kwargs.pop('class_', '')
            kwargs['class'] = '%s %s' % (self.error_class, c)

        if not 'placeholder' in kwargs:
            kwargs['placeholder'] = field.label.text
        return super(SlTextArea, self).__call__(field, **kwargs)

class SlPasswordInput(SlInput):
    input_type = 'password'

    def __init__(self, hide_value=True, **kwargs):
        super(SlPasswordInput, self).__init__(**kwargs)
        self.hide_value = hide_value

    def __call__(self, field, **kwargs):
        if self.hide_value:
            kwargs['value'] = ''
        return super(SlPasswordInput, self).__call__(field, **kwargs)

class SlCheckboxInput(SlInput):
    input_type = 'checkbox'

    def __call__(self, field, **kwargs):
        if getattr(field, 'checked', field.data):
            kwargs['checked'] = True
        return super(SlCheckboxInput, self).__call__(field, **kwargs)

class SlNumberInput(SlInput):
    input_type = 'number'
