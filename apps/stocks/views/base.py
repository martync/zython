# -*- coding: utf-8 -*-
from django import http
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from brew.models import Malt, Hop, Yeast
from units.views import UnitViewFormMixin
from ..forms import StockMaltForm, StockHopForm, StockYeastForm
from ..choices import INGREDIENT_MALT, INGREDIENT_HOP, INGREDIENT_YEAST, INGREDIENTS_DICT


SLUG_MODELS = {
    INGREDIENT_MALT: Malt,
    INGREDIENT_HOP: Hop,
    INGREDIENT_YEAST: Yeast
}


SLUG_FORMS = {
    INGREDIENT_MALT: StockMaltForm,
    INGREDIENT_HOP: StockHopForm,
    INGREDIENT_YEAST: StockYeastForm
}

FORMS_SPLIT_COLUMS = {
    INGREDIENT_MALT: 4,
    INGREDIENT_HOP: 4,
    INGREDIENT_YEAST: 12
}


class BaseStockMixin(object):

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(BaseStockMixin, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(BaseStockMixin, self).get_context_data(**kwargs)
        context["ingredients_dict"] = INGREDIENTS_DICT
        return context


class BaseIngredientViewMixin(object):
    def dispatch(self, request, *args, **kwargs):
        if kwargs["ingredient"] not in SLUG_MODELS:
            raise http.Http404
        self.ingredient = kwargs["ingredient"]
        self.model = SLUG_MODELS[kwargs["ingredient"]]
        self.form = SLUG_FORMS[kwargs["ingredient"]]
        return super(BaseIngredientViewMixin, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(BaseIngredientViewMixin, self).get_context_data(**kwargs)
        context["ingredient"] = self.ingredient
        context["ingredient_term"] = INGREDIENTS_DICT[self.ingredient]
        return context

    def get_queryset(self):
        return self.model.objects.filter(stock_user=self.request.user).order_by("-stock_added", )


class BaseStockIngredientFormMixin(UnitViewFormMixin):
    def get_template_names(self):
        return "stocks/ingredient_form.html"

    def get_form_class(self):
        return self.form

    def get_context_data(self, **kwargs):
        context = super(BaseStockIngredientFormMixin, self).get_context_data(**kwargs)
        context["split_column_at"] = FORMS_SPLIT_COLUMS[self.ingredient]
        return context

    def get_form_kwargs(self):
        kwargs = super(BaseStockIngredientFormMixin, self).get_form_kwargs()
        if not "instance" in kwargs:
            kwargs["instance"] = self.model()
        if not kwargs["instance"]:
            kwargs["instance"] = self.model()
        kwargs["instance"].stock_user = self.request.user
        return kwargs
