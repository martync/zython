from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django import http

from fm.views import AjaxCreateView, AjaxUpdateView
from units.views import UnitViewFormMixin

from ..decorators import recipe_author
from ..forms import MashStepForm
from ..models import MashStep
from .base import RecipeAuthorMixin


__all__ = (
    "MashCreateView", "MashUpdateView", "mash_delete"
)


class MashFormMixin(RecipeAuthorMixin):
    template_name = "brew/mashstep_form.html"
    form_class = MashStepForm
    model = MashStep

    def form_valid(self, form):
        form.save()
        return super(MashFormMixin, self).form_valid(form)


class MashCreateView(MashFormMixin, AjaxCreateView):

    def get_form_kwargs(self):
        kwargs = super(MashCreateView, self).get_form_kwargs()
        ordering = self.recipe.mashstep_set.all().count() + 1
        kwargs["instance"] = MashStep(recipe=self.recipe, ordering=ordering)
        initial = kwargs.get("initial", None) or {}

        if not self.recipe.mashstep_set.all().count():
            initial["water_added"] = "%.2f" % self.recipe.water_initial_mash()
            initial["name"] = "Mash in"
            initial["step_type"] = "temperature"
            initial["temperature"] = "66.0"
            initial["step_time"] = "60"
            initial["rise_time"] = "10"
        else:
            initial["step_type"] = "temperature"
            initial["water_added"] = "0"
            initial["name"] = "Mash step"
            initial["rise_time"] = "10"
        kwargs["initial"] = initial
        kwargs["request"] = self.request
        return kwargs


class MashUpdateView(MashFormMixin, UnitViewFormMixin, AjaxUpdateView):
    pk_url_kwarg = 'object_id'
    template_name_suffix = "_form"


@login_required
@recipe_author
def mash_delete(request, recipe, recipe_id, object_id):
    mash = get_object_or_404(MashStep, pk=object_id, recipe=recipe)
    mash.delete()
    return http.HttpResponseRedirect(recipe.get_absolute_url())
