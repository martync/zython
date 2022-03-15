from django import template
from units import settings as app_settings
from units.helpers import get_converted_value
register = template.Library()


class LocalUnitNode(template.Node):
    def __init__(self, unit_group, value, long_term):
        self.unit_group = unit_group
        self.long_term = long_term
        self.value = template.Variable(value)

    def render(self, context):
        value = self.value.resolve(context)
        long_term = self.long_term
        request = context['request']
        unit_group = self.unit_group
        key = "%s%s" % (
            app_settings.CONTEXT_PREFIX,
            unit_group
        )
        user_unit = request.session.get(key)
        return get_converted_value(value, user_unit, unit_group, long_term)


@register.simple_tag
def do_local_unit(parser, token):
    """
    {% local_unit "volume" stuff.water %}
    """
    length = len(token.split_contents())
    if length == 3:
        tag_name, unit_group, value = token.split_contents()
        long_term = True
    elif length == 4:
        tag_name, unit_group, value, long_term = token.split_contents()
        long_term = int(long_term)
    else:
        raise template.TemplateSyntaxError("%r tag requires exactly two or three arguments" % token.contents.split()[0])
    if not (unit_group[0] == unit_group[-1] and unit_group[0] in ('"', "'")):
        raise template.TemplateSyntaxError("%r tag's argument should be in quotes" % tag_name)
    return LocalUnitNode(unit_group[1:-1], value, long_term)
register.tag('local_unit', do_local_unit)
