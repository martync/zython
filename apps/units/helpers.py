from units import settings as app_settings
from units import conversions


def get_converted_value(value, user_unit, group, long_term=True, raw_output=False, reverse=False):
    unit_group = app_settings.UNITS.get(group)
    source_unit = unit_group.get('default')
    precision = "%" + ".%sf" % unit_group.get('precision', 1)
    choices = dict((x, y) for x, y in unit_group.get('choices'))
    if long_term == 1:
        verbose_unit = choices.get(user_unit, user_unit)
    elif long_term == 0:
        verbose_unit = user_unit
    elif long_term == -1:
        verbose_unit = ""
    if source_unit != user_unit:
        function = '%s_to_%s' % (source_unit, user_unit)
        if reverse:
            function = '%s_to_%s' % (user_unit, source_unit)
        if hasattr(conversions, function):
            convers_function = getattr(conversions, function)
            value = convers_function(value)
        else:
            value = None
    if value == "" or value is None:
        return ""
    value = precision % float(value)
    if raw_output:
        return value
    return u"%s %s" % (value, verbose_unit)


def get_full_unit_name(group_name, unit_short):
    unit_group = app_settings.UNITS.get(group_name)
    return dict(unit_group.get('choices')).get(unit_short)


def get_convert_to_default(*args, **kwargs):
    return get_converted_value(reverse=True, *args, **kwargs)
