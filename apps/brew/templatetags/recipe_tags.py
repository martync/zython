from django.utils.translation import ugettext_lazy as _
from django import template
from public.helpers import CsvToTxt
from units import settings as app_settings
from units.helpers import get_converted_value
register = template.Library()


class RecipeIngredientTxt(template.Node):
    def __init__(self, recipe):
        self.recipe = template.Variable(recipe)

    def render(self, context):
        self.recipe = self.recipe.resolve(context)
        request = context['request']
        key = "%s%s" % (app_settings.CONTEXT_PREFIX, "weight")
        weight_unit = request.session.get("%s%s" % (app_settings.CONTEXT_PREFIX, "weight"))
        hop_unit = request.session.get("%s%s" % (app_settings.CONTEXT_PREFIX, "hop"))
        volume_unit = request.session.get("%s%s" % (app_settings.CONTEXT_PREFIX, "volume"))
        temperature_unit = request.session.get("%s%s" % (app_settings.CONTEXT_PREFIX, "temperature"))
        color_unit = request.session.get("%s%s" % (app_settings.CONTEXT_PREFIX, "color"))
        i = 0
        lines = []
        # --- MALT ---
        # ------------
        for malt in self.recipe.recipemalt_set.all():
            i += 1
            line = [
                get_converted_value(malt.amount, weight_unit, "weight", 0),
                "%s (%s)" % (malt.name, get_converted_value(malt.color, color_unit, "color")),
                _(u"Grain"),
                i,
                "%s" % malt.percent() + "%"
            ]
            lines.append(";".join([str(a) for a in line]))

        # --- HOPS ---
        # ------------
        for hop in self.recipe.recipehop_set.all():
            i += 1
            line = [
                get_converted_value(hop.amount, hop_unit, "hop", 0),
                "%s (%s" % (hop.name, hop.acid_alpha) + "%) " + "- %s %s" % (hop.get_usage_display(), hop.unit_time()),
                _(u"Hop"),
                i,
                "%.1f" % hop.ibu() + " IBUs"
            ]
            lines.append(";".join([str(a) for a in line]))

        # --- MISC ---
        # ------------
        for misc in self.recipe.recipemisc_set.all():
            i += 1
            line = [
                get_converted_value(misc.amount, hop_unit, "hop", 0),
                "%s - (%s %s %s)" % (misc.name, misc.usage, misc.time, misc.time_unit),
                misc.get_misc_type_display(),
                i,
                "-"
            ]
            lines.append(";".join([str(a) for a in line]))
        csv_lines = "\n".join([str(a) for a in lines])
        csv = CsvToTxt(csv_lines, delimiter=";")
        return csv.render()


class RecipeMashStepsTxt(template.Node):
    def __init__(self, recipe):
        self.recipe = template.Variable(recipe)

    def render(self, context):
        self.recipe = self.recipe.resolve(context)
        request = context['request']
        key = "%s%s" % (app_settings.CONTEXT_PREFIX, "weight")
        volume_unit = request.session.get("%s%s" % (app_settings.CONTEXT_PREFIX, "volume"))
        temperature_unit = request.session.get("%s%s" % (app_settings.CONTEXT_PREFIX, "temperature"))
        i = 0
        lines = []
        for step in self.recipe.mashstep_set.all():
            i += 1
            description = ""
            if step.water_added:
                description = _(
                    u"Add %(water)s of water" % {
                        'water':
                        get_converted_value(step.water_added, volume_unit, "volume", 0),
                    }
                ) + ". "

            step_temperature = get_converted_value(step.temperature, temperature_unit, "temperature", 0)
            temperature = step_temperature
            if i == 1:
                temperature = get_converted_value(step.initial_heat(), temperature_unit, "temperature", 0)
            description += u"%s" % _('Heat over') + " "
            description += str(temperature)
            line = [
                step.name,
                description,
                step_temperature,
                "%s min" % step.step_time
            ]
            lines.append(";".join([str(a) for a in line]))
        csv_lines = "\n".join([str(a) for a in lines])
        csv = CsvToTxt(csv_lines, delimiter=";")
        return csv.render()


@register.simple_tag
def recipe_ingredients_txt(parser, token):
    """
    {% recipe_ingredients_txt recipe %}
    """
    length = len(token.split_contents())
    if length == 2:
        tag_name, recipe = token.split_contents()
    else:
        raise template.TemplateSyntaxError("%r tag requires exactly two arguments" % token.contents.split()[0])
    return RecipeIngredientTxt(recipe)
register.tag('recipe_ingredients_txt', recipe_ingredients_txt)


@register.simple_tag
def recipe_mashsteps_txt(parser, token):
    """
    {% recipe_mashsteps_txt recipe %}
    """
    length = len(token.split_contents())
    if length == 2:
        tag_name, recipe = token.split_contents()
    else:
        raise template.TemplateSyntaxError("%r tag requires exactly two arguments" % token.contents.split()[0])
    return RecipeMashStepsTxt(recipe)
register.tag('recipe_mashsteps_txt', recipe_mashsteps_txt)


@register.filter
def rangeable(value):
    if not value:
        return ""
    return int(float(value) * 1000)
