from django import http
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required

from fm.views import AjaxCreateView, AjaxUpdateView
import djnext

from public.utils.views import FormViewWithRequestMixin
from .base import RecipeAuthorMixin, SLUG_MODEL, SLUG_MODELFORM
from ..decorators import recipe_author


__all__ = (
    "IngredientCreateView", "IngredientUpdateView", "remove_ingredient",
)


class IngredientFormMixin(RecipeAuthorMixin, FormViewWithRequestMixin):

    def dispatch(self, *args, **kwargs):
        self.ingredient = kwargs.get("ingredient")
        if self.ingredient not in SLUG_MODEL:
            raise http.Http404
        self.ingredient_model = SLUG_MODEL[self.ingredient]
        response = super(IngredientFormMixin, self).dispatch(*args, **kwargs)
        return response

    def get_template_names(self):
        return "brew/raw_%(ingredient)s_form.html" % self.kwargs

    def get_form_class(self):
        return SLUG_MODELFORM[self.kwargs["ingredient"]]

    def get_success_url(self):
        return self.recipe.get_absolute_url()

    def get_form_kwargs(self):
        kwargs = super(IngredientFormMixin, self).get_form_kwargs()
        kwargs["instance"] = self.get_instance()
        return kwargs


class IngredientCreateView(IngredientFormMixin, AjaxCreateView):

    def get_instance(self):
        return self.ingredient_model(**self.get_instance_kwargs())

    def get_instance_kwargs(self):
        return {"recipe": self.recipe, }


class IngredientUpdateView(IngredientFormMixin, AjaxUpdateView):

    def get_instance(self):
        return get_object_or_404(self.ingredient_model, pk=self.kwargs["object_id"], recipe=self.recipe)


@login_required
@recipe_author
def remove_ingredient(request, recipe, recipe_id, ingredient, object_id):
    model_class = SLUG_MODEL[ingredient]
    ingredient = get_object_or_404(model_class, pk=object_id, recipe=recipe)
    ingredient.delete()
    next = djnext.ref_get_post(request, recipe.get_absolute_url())
    return http.HttpResponseRedirect(next)
