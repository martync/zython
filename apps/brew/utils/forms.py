from django.forms import widgets

BS3_FORM_CONTROL_SUBTYPES = (
    widgets.TextInput,
    widgets.PasswordInput,
    widgets.Textarea,
    widgets.Select,
    widgets.FileInput,
    widgets.SelectMultiple,

)


class BS3FormBaseMixin(object):
    css_class = "form-control"

    @classmethod
    def add_bs3_properties(cls, field):
        widget = field.widget
        current_attrs = widget.attrs or {}
        existing_class = current_attrs.get('class', '')
        if 'no_BS3' not in existing_class:
            field.widget.attrs.update({'class': "%s %s" % (cls.css_class, existing_class)})

    def _apply_formatting(self):
        for field in self:
            k = field.name
            widget = self.fields[k].widget
            if "Check" in u"%s" % widget.__class__:
                continue
            for t in BS3_FORM_CONTROL_SUBTYPES:
                if issubclass(widget.__class__, t):
                    self.add_bs3_properties(self.fields[k])

    def __init__(self, *args, **kwargs):
        super(BS3FormBaseMixin, self).__init__(*args, **kwargs)
        self._apply_formatting()


class BS3FormMixin(BS3FormBaseMixin):
    css_class = "form-control"


class BS3FormFullMixin(BS3FormBaseMixin):
    css_class = "form-control full-field"
