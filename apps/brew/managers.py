from django.conf import settings
from django.db import models
from django.db.models.query import QuerySet
from django.db.models import Q
from guardian.shortcuts import get_objects_for_user


class IngredientQueryset(QuerySet):
    def stocked(self, user):
        return self.filter(stock_user=user)

    def public_and_stocked(self, user):
        return self.filter(
            Q(stock_user__isnull=True) |
            Q(stock_user=user, stock_amount__gt=0)
        ).order_by("-stock_user")


class IngredientManager(models.Manager):
    def get_queryset(self):
        return IngredientQueryset(self.model, using=self._db)


class RecipeManager(models.Manager):
    def for_user(self, user):
        qs = self.get_queryset()
        if user.is_active:
            special_recipes = get_objects_for_user(user, 'brew.view_recipe')
            qs = qs.filter(
                Q(private=False) |
                Q(user=user) |
                Q(id__in=[r.id for r in special_recipes])
            )
        else:
            qs = qs.filter(private=False)
        return qs


class BeerStyleManager(models.Manager):
    def get_active_styles(self):
        return self.get_queryset().filter(guide=settings.ACTIVE_BJCP_YEAR)
