from django import forms
from django.utils.translation import ugettext_lazy as _
from django.db.models import Q
from units.forms import UnitModelForm, UnitForm
from .models import *
from .settings import MAIN_STYLES
from .utils.forms import BS3FormMixin

__all__ = (
    'RecipeForm', 'RecipeMaltForm', 'RecipeHopForm',
    'RecipeMiscForm', 'RecipeYeastForm', 'MashStepForm',
    'RecipeImportForm', 'RecipeSearchForm'
)


def style_choices(qs_kwargs=None):
    if not qs_kwargs:
        qs_kwargs = {}
    old_number = 0
    item = ("", "-------")
    items = []
    for s in BeerStyle.objects.filter(**qs_kwargs).distinct():
        number = s.number
        if old_number != number:
            items.append(item)
            item = [MAIN_STYLES[str(number)], []]
        item[1].append((s.id, "%s" % s))
        old_number = number
    items.append(item)
    return items


class RecipeForm(BS3FormMixin, UnitModelForm):
    unit_fields = {
        'volume': [
            'batch_size',
            'boiler_tun_deadspace',
            'mash_tun_deadspace'
        ],
        'temperature': ['grain_temperature', ]
    }
    recipe_style = forms.ChoiceField(
        label="Style", choices=(), required=False)

    def __init__(self, *args, **kwargs):
        super(RecipeForm, self).__init__(*args, **kwargs)
        batch_size_css_class = self.fields["batch_size"].widget.attrs.get("class", "")
        name_css_class = self.fields["name"].widget.attrs.get("class", "")
        self.fields["batch_size"].widget.attrs.update({"class":"{} input-lg".format(batch_size_css_class)})
        self.fields["name"].widget.attrs.update({"class":"{} input-lg".format(name_css_class)})
        self.fields["recipe_style"].choices = style_choices()

        if self.instance.style:
            self.initial['recipe_style'] = str(self.instance.style.pk)

    def save(self, *args, **kwargs):
        recipe = super(RecipeForm, self).save(*args, **kwargs)
        datas = self.cleaned_data
        if datas['recipe_style']:
            recipe.style = BeerStyle.objects.get(pk=datas['recipe_style'])
        recipe.update_slug_url()
        return recipe

    class Meta:
        model = Recipe
        fields = (
            'name', 'batch_size', 'efficiency', 'private',
            'recipe_style', 'recipe_type',
            'mash_tun_deadspace', 'boiler_tun_deadspace',
            'evaporation_rate', 'grain_temperature'
        )


class RecipeImportForm(forms.Form):
    beer_file = forms.FileField(label=_("Your recipe (BeerXML format)"))


class RecipeIngredientForm(BS3FormMixin, UnitModelForm):
    def __init__(self, *args, **kwargs):
        super(RecipeIngredientForm, self).__init__(*args, **kwargs)
        if hasattr(self, "addition_stock_field"):
            self.fields["%s_id" % self.addition_stock_field[0]] = forms.IntegerField(required=False, widget=forms.HiddenInput())

    def save(self, *args, **kwargs):
        obj = super(RecipeIngredientForm, self).save(*args, **kwargs)
        if hasattr(self, "addition_stock_field"):
            obj_id = self.data.get("%s_id" % self.addition_stock_field[0])
            if obj_id:
                model_name = self.addition_stock_field[1]
                try:
                    source_obj = model_name.objects.get(pk=obj_id, stock_user=self.request.user, stock_amount__gt=0)  # Filter only stocked items
                    setattr(obj, self.addition_stock_field[0], source_obj)
                    obj.save()
                except model_name.DoesNotExist:
                    pass
        return obj


class RecipeMaltForm(RecipeIngredientForm):
    unit_fields = {'weight': ['amount', ], 'color': ['color', ]}
    addition_stock_field = ["malt", Malt]

    def get_ingredient_list(self):
        return Malt.objects.all().public_and_stocked(self.request.user)

    class Meta:
        model = RecipeMalt
        fields = (
            'amount', 'color',
            'name', 'origin', 'malt_type',
            'potential_gravity', 'malt_yield', 'diastatic_power',
            'protein', 'max_in_batch', 'notes',
        )


class RecipeHopForm(RecipeIngredientForm):
    unit_fields = {'hop': ['amount', ]}
    addition_stock_field = ["hop", Hop]

    def get_ingredient_list(self):
        return Hop.objects.all().public_and_stocked(self.request.user)

    def clean(self):
        data = self.cleaned_data
        if data.get('usage') == "dryhop" and not data.get('dry_days'):
            msg = _("Please enter a number of days of dry hoping")
            self._errors["dry_days"] = self.error_class([msg])
        return data

    class Meta:
        model = RecipeHop
        fields = (
            'amount', 'boil_time', 'dry_days', 'acid_alpha',
            'name', 'origin', 'usage', 'form', 'hop_type',
            'acid_alpha', 'acid_beta', 'notes'
        )


class RecipeMiscForm(RecipeIngredientForm):
    unit_fields = {'hop': ['amount', ]}

    def get_ingredient_list(self):
        return Misc.objects.all()

    class Meta:
        model = RecipeMisc
        fields = (
            'amount', 'use_in', 'time',
            'time_unit', 'name', 'misc_type',
            'usage', 'notes'
        )


class RecipeYeastForm(RecipeIngredientForm):
    addition_stock_field = ["yeast", Yeast]

    def get_ingredient_list(self):
        return Yeast.objects.all().public_and_stocked(self.request.user)

    class Meta:
        model = RecipeYeast
        fields = (
            'name', 'laboratory', 'product_id',
            'yeast_type', 'form', 'flocculation',
            'min_attenuation', 'max_attenuation',
            'min_temperature', 'max_temperature',
            'best_for', 'notes'
        )


class MashStepForm(BS3FormMixin, UnitModelForm):
    unit_fields = {
        'volume': ['water_added', ],
        'temperature': ['temperature', ],
    }

    class Meta:
        model = MashStep
        fields = (
            'name', 'step_type', 'temperature',
            'step_time', 'rise_time', 'water_added'
        )


class RecipeSearchForm(forms.Form):
    style = forms.ChoiceField(
        label=_(u"Style"),
        choices=(),
        required=False
    )
    q = forms.CharField(required=False)

    def __init__(self, *args, **kwargs):
        super(RecipeSearchForm, self).__init__(*args, **kwargs)
        self.fields["style"].choices = style_choices(qs_kwargs={'recipe__id__isnull': False})


    def search(self, qs):
        data = self.cleaned_data
        if data['style']:
            qs = qs.filter(style=data['style'])
        if data['q']:
            q = data['q']
            qs = qs.filter(
                Q(name__icontains=q) |
                Q(user__username__icontains=q) |
                Q(style__name__icontains=q) |
                Q(recipemalt__name__icontains=q) |
                Q(recipehop__name__icontains=q) |
                Q(recipemisc__name__icontains=q) |
                Q(recipeyeast__name__icontains=q)
            )
        return qs.distinct()


class EfficiencyCalculatorForm(UnitForm):
    """ form used for the inline effective efficiency computation"""
    unit_fields = {
        "volume": ["collected_volume", ]
        # no unit for density/gravity
    }
    collected_volume = forms.FloatField(label=_(u"Collected Volume"))
    measured_gravity = forms.FloatField(label=_(u"Measured OG"))
