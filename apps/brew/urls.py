from django.urls import re_path
from django.contrib.auth.decorators import login_required
from .views import *
from .forms import *
from .models import *

urlpatterns = [
    re_path(r'^add/$',
        RecipeCreateView.as_view(),
        name='brew_recipe_add'),

    re_path(r'^import/$',
        RecipeImportView.as_view(),
        name='brew_recipe_import'),

    re_path(r'^user/(?P<username>\w+)/$',
        RecipeListView.as_view(),
        name='brew_recipe_user'),

    re_path(r'^my-recipes/$',
        login_required(UserRecipeListView.as_view()),
        name='brew_recipe_owner'),

    re_path(r'^user/$',
        UserListView.as_view(),
        name='brew_recipe_users'),

    re_path(r'^by-style/$',
        StyleRecipesView.as_view(),
        name="brew_recipe_styles"),

    re_path(r'^by-style/(?P<slug>[\w-]+)-(?P<pk>\d+)/$',
        StyleRecipeView.as_view(),
        name="brew_recipe_style"),

    re_path(r'^(?P<pk>\d+)-(?P<slug>[\w-]+)/$',
        RecipeDetailView.as_view(),
        name='brew_recipe_detail'),

    re_path(r'^(?P<pk>\d+)-(?P<slug>[\w-]+)/comments/$',
        RecipeDetailView.as_view(page="comments"),
        name='brew_recipe_comments'),

    re_path(r'^(?P<pk>\d+)-(?P<slug>[\w-]+)/permissions/$',
        RecipeDetailView.as_view(page="permissions"),
        name='brew_recipe_permissions'),

    re_path(r'^(?P<recipe_id>\d+)-(?P<slug>[\w-]+)/permissions/set/$',
        set_user_perm,
        name='brew_recipe_setperms'),

    re_path(r'^(?P<pk>\d+)-(?P<slug>[\w-]+)/print/$',
        RecipeDetailView.as_view(page="print"),
        name='brew_recipe_print'),

    re_path(r'^(?P<pk>\d+)-(?P<slug>[\w-]+)/text/$',
        RecipeDetailView.as_view(page="text"),
        name='brew_recipe_text'),

    re_path(r'^(?P<recipe_id>\d+)-(?P<slug>[\w-]+)/confirm-delete/$',
        RecipeDeleteView.as_view(),
        name='brew_recipe_delete'),

    re_path(r'^(?P<recipe_id>\d+)-(?P<slug>[\w-]+)/destock/$',
        RecipeDestockView.as_view(),
        name='brew_recipe_destock'),

    re_path(r'^(?P<recipe_id>\d+)-(?P<slug>[\w-]+)/edit/$',
        RecipeUpdateView.as_view(),
        name='brew_recipe_edit'),

    re_path(r'^(?P<recipe_id>\d+)-(?P<slug>[\w-]+)/clone/$',
        RecipeCloneView.as_view(),
        name='brew_recipe_clone'),

    re_path(r'^(?P<recipe_id>\d+)-(?P<slug>[\w-]+)/calculator$',
        RecipeEfficiencyCalculatorView.as_view(),
        name='brew_recipe_efficiency_calculator'),

    re_path(r'^(?P<recipe_id>\d+)/add/(?P<ingredient>\w+)/$',
        IngredientCreateView.as_view(),
        name='brew_recipe_addingredient'),

    re_path(r'^(?P<recipe_id>\d+)/remove/(?P<ingredient>\w+)/(?P<object_id>\d+)/$',
        remove_ingredient,
        name='brew_recipe_removeingredient'),

    re_path(r'^(?P<recipe_id>\d+)/edit/(?P<ingredient>\w+)/(?P<object_id>\d+)/$',
        IngredientUpdateView.as_view(),
        name='brew_recipe_editingredient'),

    re_path(r'^(?P<recipe_id>\d+)/mash/add/$',
        MashCreateView.as_view(),
        name="brew_mash_add"),

    re_path(r'^(?P<recipe_id>\d+)/mash/(?P<object_id>\d+)/edit/$',
        MashUpdateView.as_view(),
        name="brew_mash_edit"),

    re_path(r'^(?P<recipe_id>\d+)/mash/(?P<object_id>\d+)/delete/$',
        mash_delete,
        name="brew_mash_delete"),

    re_path(r'^guide/style/$',
        StyleListView.as_view(),
        name="brew_style_list"),

    re_path(r'^guide/style/(?P<pk>\d+)/$',
        StyleDetailView.as_view(),
        name="brew_style_detail")
]
