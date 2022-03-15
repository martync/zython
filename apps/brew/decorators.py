#-*- encoding:utf-8 -*-
from django.http import HttpResponseRedirect
from .models import Recipe


def recipe_author(f, redirect_url="/"):
    def wrap(request, *args, **kwargs):
        recipe_id = kwargs.get('recipe_id')
        try:
            recipe = Recipe.objects.get(pk=recipe_id)
            if recipe.user == request.user or request.user.has_perm('change_recipe', recipe):
                return f(request, recipe, *args, **kwargs)
        except Recipe.DoesNotExist:
            pass
        return HttpResponseRedirect("/")

    # wrap.__doc__ = f.__doc__
    # wrap.__name__ = f.__name__
    return wrap
