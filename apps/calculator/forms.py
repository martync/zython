from django import forms
from django.utils.translation import ugettext_lazy as _
from django.template import loader
from brew import formulas
from units.forms import UnitForm


class ABVForm(UnitForm):
    unit_fields = {
        'temperature': ['temperature', ],
    }

    og = forms.DecimalField(label=_(u"Original gravity"), help_text=_("For example : 1.090"))
    fg = forms.DecimalField(label=_(u"Final gravity"), help_text=_("For example : 1.012"))
    temperature = forms.IntegerField(label=_(u"Temperature"))

    def get_results(self):
        abv = formulas.get_abv(
            self.cleaned_data["og"],
            self.cleaned_data["fg"],
            self.cleaned_data["temperature"],
        )
        return loader.render_to_string("calculator/abv_results.html", {"abv": abv})

