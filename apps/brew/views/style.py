from django.views.generic import ListView,  DetailView
from django.shortcuts import get_object_or_404
from django.db.models import Q

from ..models import BeerStyle, Recipe
from .recipe import RecipeListView


__all__ = ("StyleRecipesView", "StyleRecipeView", "StyleListView", "StyleDetailView")


class StyleRecipesView(ListView):
    model = BeerStyle
    template_name = "brew/style_list.html"

    def get_queryset(self):
        qs = super(StyleRecipesView, self).get_queryset()
        return qs.filter(recipe__private=False).distinct()


class StyleRecipeView(RecipeListView):
    template_name = "brew/style_recipe_list.html"

    def get_context_data(self, **kwargs):
        context = super(StyleRecipeView, self).get_context_data(**kwargs)
        context["style"] = get_object_or_404(BeerStyle.objects, pk=self.kwargs["pk"])
        return context

    def get_queryset(self):
        qs = super(StyleRecipeView, self).get_queryset().filter(style__pk=self.kwargs["pk"])
        return qs


class StyleListView(ListView):
    model = BeerStyle


class StyleDetailView(DetailView):
    model = BeerStyle

    def get_context_data(self, **kwargs):
        context = super(StyleDetailView, self).get_context_data(**kwargs)
        queryset = Recipe.objects.filter(style=self.object).select_related('user', 'style')
        if self.request.user.is_active:
            qs = queryset.filter(
                Q(private=False) | Q(user=self.request.user)
            )
        else:
            qs = queryset.filter(private=False)
        context['related_recipes'] = qs
        context['same_category_styles'] = BeerStyle.objects.filter(
            category=self.object.category
        ).exclude(id=self.object.id)
        return context
