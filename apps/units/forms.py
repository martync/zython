from django import forms
from units import settings as app_settings
from units.helpers import get_convert_to_default, get_full_unit_name, get_converted_value


class BaseUnitForm(object):
    unit_fields = {}
    '''
    unit_fields = {
        'volume': ['amount', 'batch_size'],
        'weight': ['total_grain']
    }
    '''

    def get_unit_fieldnames(self):
        fieldnames = []
        if self.unit_fields:
            for group,fields in self.unit_fields.items():
                for f in fields:
                    fieldnames.append(f)
        return fieldnames

    def __init__(self, request, *args, **kwargs):
        self.request = request
        super(BaseUnitForm, self).__init__(*args, **kwargs)
        prefix = app_settings.CONTEXT_PREFIX
        for group,fields in self.unit_fields.items():
            user_unit = self.request.session.get('%s%s' % (prefix, group))
            for f in fields:
                unit_group = app_settings.UNITS.get(group)
                help_text = get_full_unit_name(group, user_unit)
                self.fields[f].help_text = user_unit
                if self.initial.get(f):
                    val = self.initial[f]
                    self.initial[f] = get_converted_value(val, user_unit, group, raw_output=True)

    def clean(self):
        datas = self.cleaned_data
        prefix = app_settings.CONTEXT_PREFIX
        for group,fields in self.unit_fields.items():
            user_unit = self.request.session.get('%s%s' % (prefix, group))
            for f in fields:
                value = datas.get(f)
                if None not in (value, user_unit):
                    v = get_convert_to_default(value, user_unit, group, raw_output=True)
                    datas[f] = v
        return datas

    def save(self, *args, **kwargs):
        return super(BaseUnitForm, self).save(*args, **kwargs)


class UnitModelForm(BaseUnitForm, forms.ModelForm):
    pass


class UnitForm(BaseUnitForm, forms.Form):
    pass
